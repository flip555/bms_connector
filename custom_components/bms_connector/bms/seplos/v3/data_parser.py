import struct
import logging

_LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# CRC Modbus RTU
# ---------------------------------------------------------------------------

def modbus_crc(data: bytes) -> bytes:
    """Calculate the Modbus RTU CRC (little-endian, 2 bytes)."""
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
    return struct.pack('<H', crc)


def verify_crc(frame_hex: str) -> bool:
    """Vérifie le CRC d'une trame Modbus reçue (format hex string)."""
    try:
        raw = bytes.fromhex(frame_hex)
        if len(raw) < 4:
            return False
        payload = raw[:-2]
        received_crc = raw[-2:]
        expected_crc = modbus_crc(payload)
        return received_crc == expected_crc
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Construction des commandes Modbus RTU
# ---------------------------------------------------------------------------

def build_read_command(addr: int, register: int, count: int) -> str:
    """
    Construit une commande Modbus RTU 0x04 (Read Input Registers).

    Args:
        addr:     Adresse esclave (0x01 à 0x7F pour un BMS SEPLOS)
        register: Adresse de début du registre (ex: 0x1000 pour PIA)
        count:    Nombre de registres à lire

    Returns:
        Trame complète en hex string (sans espaces), CRC inclus.
    """
    payload = bytes([addr, 0x04]) + struct.pack('>HH', register, count)
    crc = modbus_crc(payload)
    cmd = (payload + crc).hex()
    _LOGGER.debug("Modbus command built: %s (addr=0x%02X, reg=0x%04X, count=%d)",
                  cmd, addr, register, count)
    return cmd


def build_commands_for_address(battery_addr: int) -> list:
    """
    Retourne la liste des commandes PIA + PIB pour une adresse de batterie donnée.

    PIA : registre 0x1000, 18 registres (0x12) — données pack global
    PIB : registre 0x1100, 26 registres (0x1A) — tensions cellules + températures
    """
    cmd_pia = build_read_command(battery_addr, 0x1000, 0x12)
    cmd_pib = build_read_command(battery_addr, 0x1100, 0x1A)
    _LOGGER.debug("Commands for battery 0x%02X: PIA=%s | PIB=%s",
                  battery_addr, cmd_pia, cmd_pib)
    return [cmd_pia, cmd_pib]


# ---------------------------------------------------------------------------
# Découverte d'adresse BMS
# ---------------------------------------------------------------------------

# Réponse PIA valide : addr(1) + 0x04(1) + byte_count(1=0x24) + data(36) + crc(2) = 41 bytes
_PIA_RESPONSE_BYTES = 41
# Hex chars for a valid PIA response: 41 bytes × 2 = 82 hex chars
_PIA_RESPONSE_HEX_LEN = _PIA_RESPONSE_BYTES * 2


def discover_bms_address(send_fn, port, baudrate=19200, max_addr=0x0F):
    """
    Scan les adresses Modbus 0x00 à max_addr pour trouver un BMS.

    Envoie une commande PIA (read 18 registres depuis 0x1000) à chaque
    adresse et vérifie si la réponse est une trame Modbus RTU valide
    avec le bon nombre de bytes de données.

    Args:
        send_fn:  Callable (commands, port, baudrate) -> [response_hex_str, ...]
        port:     Port série (ex: "/dev/ttyUSB0")
        baudrate: Débit en bauds
        max_addr: Adresse maximale à tester (défaut 0x0F)

    Returns:
        (int | None) Adresse trouvée, ou None si aucune.
    """
    _LOGGER.info("Scanning for BMS on %s (addresses 0x00–0x%02X)...", port, max_addr)

    for addr in range(max_addr + 1):
        cmd = build_read_command(addr, 0x1000, 0x12)
        responses = send_fn([cmd], port, baudrate)

        if not responses or not responses[0]:
            _LOGGER.debug("Address 0x%02X: no response", addr)
            continue

        response = responses[0]

        # Vérification rapide : longueur suffisante ?
        if len(response) < _PIA_RESPONSE_HEX_LEN:
            _LOGGER.debug(
                "Address 0x%02X: response too short (%d chars, expected %d)",
                addr, len(response), _PIA_RESPONSE_HEX_LEN
            )
            continue

        # Vérification : le premier byte doit correspondre à l'adresse
        if not response.startswith(f"{addr:02x}"):
            _LOGGER.debug(
                "Address 0x%02X: response starts with unexpected addr byte 0x%s",
                addr, response[:2]
            )
            continue

        # Vérification : function code doit être 0x04
        if response[2:4] != "04":
            _LOGGER.debug(
                "Address 0x%02X: unexpected function code 0x%s",
                addr, response[2:4]
            )
            continue

        # Vérification : byte_count doit être 0x24 (36 bytes de données pour PIA)
        if response[4:6] != "24":
            _LOGGER.debug(
                "Address 0x%02X: unexpected byte_count 0x%s",
                addr, response[4:6]
            )
            continue

        # Vérification CRC
        if not verify_crc(response):
            _LOGGER.debug("Address 0x%02X: CRC invalid", addr)
            continue

        _LOGGER.info(
            "BMS found at address 0x%02X — valid PIA response (%d chars)",
            addr, len(response)
        )
        return addr

    _LOGGER.warning(
        "No BMS found on %s scanning addresses 0x00–0x%02X",
        port, max_addr
    )
    return None


# ---------------------------------------------------------------------------
# Conversion de types Modbus
# ---------------------------------------------------------------------------

def convert_bytes_to_data(data_type: str, byte1: int, byte2: int):
    """
    Convertit deux bytes en valeur typée.

    Args:
        data_type: "UINT16" ou "INT16"
        byte1:     Byte de poids fort (MSB)
        byte2:     Byte de poids faible (LSB)
    """
    if data_type == "UINT16":
        return (byte1 << 8) | byte2
    elif data_type == "INT16":
        value = (byte1 << 8) | byte2
        if value & 0x8000:
            value -= 0x10000
        return value
    return None


# ---------------------------------------------------------------------------
# Structures de données
# ---------------------------------------------------------------------------

class V3PIATableData:
    """Données Pack Info A : informations générales du pack batterie."""

    def __init__(self):
        self.pack_voltage = 0            # V
        self.current = 0                 # A  (négatif = décharge)
        self.remaining_capacity = 0      # Ah
        self.total_capacity = 0          # Ah
        self.total_discharge_capacity = 0  # Ah  (cumulatif)
        self.soc = 0                     # %
        self.soh = 0                     # %
        self.cycle = 0                   # nombre de cycles
        self.avg_cell_voltage = 0        # V
        self.avg_cell_temperature = 0    # °C
        self.max_cell_voltage = 0        # V
        self.min_cell_voltage = 0        # V
        self.max_cell_temperature = 0    # °C
        self.min_cell_temperature = 0    # °C
        self.max_discharge_current = 0   # A
        self.max_charge_current = 0      # A

    def __str__(self):
        return (
            f"pack_voltage={self.pack_voltage}V, "
            f"current={self.current}A, "
            f"remaining={self.remaining_capacity}Ah, "
            f"total={self.total_capacity}Ah, "
            f"discharge_total={self.total_discharge_capacity}Ah, "
            f"soc={self.soc}%, soh={self.soh}%, cycle={self.cycle}, "
            f"avg_cell_v={self.avg_cell_voltage}V, "
            f"avg_cell_t={self.avg_cell_temperature}°C, "
            f"max_cell_v={self.max_cell_voltage}V, "
            f"min_cell_v={self.min_cell_voltage}V, "
            f"max_cell_t={self.max_cell_temperature}°C, "
            f"min_cell_t={self.min_cell_temperature}°C"
        )


class V3PIBTableData:
    """Données Pack Info B : tensions des cellules et températures."""

    def __init__(self):
        # Tensions cellules (V)
        self.cell1_voltage = 0
        self.cell2_voltage = 0
        self.cell3_voltage = 0
        self.cell4_voltage = 0
        self.cell5_voltage = 0
        self.cell6_voltage = 0
        self.cell7_voltage = 0
        self.cell8_voltage = 0
        self.cell9_voltage = 0
        self.cell10_voltage = 0
        self.cell11_voltage = 0
        self.cell12_voltage = 0
        self.cell13_voltage = 0
        self.cell14_voltage = 0
        self.cell15_voltage = 0
        self.cell16_voltage = 0
        # Températures cellules (°C)
        self.cell_temperature_1 = 0
        self.cell_temperature_2 = 0
        self.cell_temperature_3 = 0
        self.cell_temperature_4 = 0
        # Températures environnement (°C)
        self.environment_temperature = 0
        self.power_temperature = 0

    def __str__(self):
        cells = ", ".join(
            f"cell{i}_v={getattr(self, f'cell{i}_voltage')}V"
            for i in range(1, 17)
        )
        return (
            f"{cells}, "
            f"temp1={self.cell_temperature_1}°C, "
            f"temp2={self.cell_temperature_2}°C, "
            f"temp3={self.cell_temperature_3}°C, "
            f"temp4={self.cell_temperature_4}°C, "
            f"env_temp={self.environment_temperature}°C, "
            f"pwr_temp={self.power_temperature}°C"
        )


# ---------------------------------------------------------------------------
# Décodage PIA
# ---------------------------------------------------------------------------

def decode_pia_table(response: str):
    """
    Décode la réponse Modbus à la commande PIA (registres 0x1000–0x1011).

    Structure de la réponse :
        Byte 0   : ADDR  (adresse esclave)
        Byte 1   : CMD   (0x04)
        Byte 2   : LEN   (nombre de bytes de données = 2 × nb_registres)
        Bytes 3…N: DATA  (valeurs des registres, MSB en premier)
        Bytes -2 : CRC   (2 bytes, little-endian, à retirer)

    Registres PIA (spec Modbus SEPLOS V3) :
        0x1000  pack_voltage              UINT16  10mV   → × 0.01  → V
        0x1001  current                   INT16   10mA   → × 0.01  → A
        0x1002  remaining_capacity        UINT16  10mAh  → × 0.01  → Ah
        0x1003  total_capacity            UINT16  10mAh  → × 0.01  → Ah
        0x1004  total_discharge_capacity  UINT16  10Ah   → × 10    → Ah
        0x1005  soc                       UINT16  0.1%   → × 0.1   → %
        0x1006  soh                       UINT16  0.1%   → × 0.1   → %
        0x1007  cycle                     UINT16  1
        0x1008  avg_cell_voltage          UINT16  1mV    → × 0.001 → V
        0x1009  avg_cell_temperature      UINT16  0.1K   → × 0.1 − 273.15 → °C
        0x100A  max_cell_voltage          UINT16  1mV    → × 0.001 → V
        0x100B  min_cell_voltage          UINT16  1mV    → × 0.001 → V
        0x100C  max_cell_temperature      UINT16  0.1K   → × 0.1 − 273.15 → °C
        0x100D  min_cell_temperature      UINT16  0.1K   → × 0.1 − 273.15 → °C
        0x100E  (réservé)
        0x100F  max_discharge_current     UINT16  1A
        0x1010  max_charge_current        UINT16  1A
        0x1011  (réservé)
    """
    if not response:
        _LOGGER.warning("decode_pia_table: empty response")
        return None

    # Retirer le préfixe '~' éventuel (protocole PYLON/ancien SEPLOS)
    if response.startswith("~"):
        response = response[1:]

    # Vérification CRC
    if not verify_crc(response):
        _LOGGER.warning("decode_pia_table: CRC invalid for frame %s", response)
        # On continue quand même mais on prévient

    try:
        raw = bytes.fromhex(response)
    except ValueError as e:
        _LOGGER.error("decode_pia_table: unable to decode hex frame: %s", e)
        return None

    # Vérifier la longueur minimale : 3 header + 36 data (18 reg × 2) + 2 CRC = 41 bytes
    if len(raw) < 41:
        _LOGGER.warning("decode_pia_table: frame too short (%d bytes, expected >= 41)", len(raw))
        return None

    # Extraction : skip header (3 bytes), retirer CRC (2 bytes)
    data = raw[3:-2]

    pia = V3PIATableData()

    try:
        pia.pack_voltage             = convert_bytes_to_data("UINT16", data[0],  data[1])  * 0.01
        pia.current                  = convert_bytes_to_data("INT16",  data[2],  data[3])  * 0.01
        pia.remaining_capacity       = convert_bytes_to_data("UINT16", data[4],  data[5])  * 0.01
        pia.total_capacity           = convert_bytes_to_data("UINT16", data[6],  data[7])  * 0.01
        # CORRECTIF : unité = 10Ah dans la spec (pas 10mAh) → ×10 pour obtenir des Ah
        pia.total_discharge_capacity = convert_bytes_to_data("UINT16", data[8],  data[9])  * 10
        pia.soc                      = convert_bytes_to_data("UINT16", data[10], data[11]) * 0.1
        pia.soh                      = convert_bytes_to_data("UINT16", data[12], data[13]) * 0.1
        pia.cycle                    = convert_bytes_to_data("UINT16", data[14], data[15])
        pia.avg_cell_voltage         = convert_bytes_to_data("UINT16", data[16], data[17]) * 0.001
        pia.avg_cell_temperature     = convert_bytes_to_data("UINT16", data[18], data[19]) * 0.1 - 273.15
        pia.max_cell_voltage         = convert_bytes_to_data("UINT16", data[20], data[21]) * 0.001
        pia.min_cell_voltage         = convert_bytes_to_data("UINT16", data[22], data[23]) * 0.001
        pia.max_cell_temperature     = convert_bytes_to_data("UINT16", data[24], data[25]) * 0.1 - 273.15
        pia.min_cell_temperature     = convert_bytes_to_data("UINT16", data[26], data[27]) * 0.1 - 273.15
        # Bytes 28-29 : réservé (0x100E)
        if len(data) >= 32:
            pia.max_discharge_current = convert_bytes_to_data("UINT16", data[30], data[31])
        if len(data) >= 34:
            pia.max_charge_current    = convert_bytes_to_data("UINT16", data[32], data[33])
    except IndexError as e:
        _LOGGER.error("decode_pia_table: index error during decoding: %s", e)
        return None

    _LOGGER.debug("PIA decoded: %s", pia)
    return pia


# ---------------------------------------------------------------------------
# Décodage PIB
# ---------------------------------------------------------------------------

def decode_pib_table(response: str):
    """
    Décode la réponse Modbus à la commande PIB (registres 0x1100–0x1119).

    Structure des données (après header, avant CRC) :
        Registres 0x1100–0x110F : tensions cellules 1–16    UINT16  1mV → × 0.001 → V
        Registres 0x1110–0x1113 : températures cellules 1–4 UINT16  0.1K → × 0.1 − 273.15 → °C
        Registres 0x1114–0x1117 : réservés
        Registre  0x1118        : température environnement  UINT16  0.1K → × 0.1 − 273.15 → °C
        Registre  0x1119        : température puissance      UINT16  0.1K → × 0.1 − 273.15 → °C

    La trame complète fait :
        3 (header) + 52 (26 reg × 2) + 2 (CRC) = 57 bytes minimum
    """
    if not response:
        _LOGGER.warning("decode_pib_table: empty response")
        return None

    if response.startswith("~"):
        response = response[1:]

    if not verify_crc(response):
        _LOGGER.warning("decode_pib_table: CRC invalid for frame %s", response)

    try:
        raw = bytes.fromhex(response)
    except ValueError as e:
        _LOGGER.error("decode_pib_table: unable to decode hex frame: %s", e)
        return None

    # Minimum : 3 header + 52 data (26 reg × 2) + 2 CRC = 57 bytes
    if len(raw) < 57:
        _LOGGER.warning("decode_pib_table: frame too short (%d bytes, expected >= 57)", len(raw))
        return None

    # Skip header (3 bytes), retirer CRC (2 bytes)
    data = raw[3:-2]

    pib = V3PIBTableData()

    try:
        # Tensions 16 cellules (registres 0x1100 à 0x110F)
        pib.cell1_voltage  = convert_bytes_to_data("UINT16", data[0],  data[1])  * 0.001
        pib.cell2_voltage  = convert_bytes_to_data("UINT16", data[2],  data[3])  * 0.001
        pib.cell3_voltage  = convert_bytes_to_data("UINT16", data[4],  data[5])  * 0.001
        pib.cell4_voltage  = convert_bytes_to_data("UINT16", data[6],  data[7])  * 0.001
        pib.cell5_voltage  = convert_bytes_to_data("UINT16", data[8],  data[9])  * 0.001
        pib.cell6_voltage  = convert_bytes_to_data("UINT16", data[10], data[11]) * 0.001
        pib.cell7_voltage  = convert_bytes_to_data("UINT16", data[12], data[13]) * 0.001
        pib.cell8_voltage  = convert_bytes_to_data("UINT16", data[14], data[15]) * 0.001
        pib.cell9_voltage  = convert_bytes_to_data("UINT16", data[16], data[17]) * 0.001
        pib.cell10_voltage = convert_bytes_to_data("UINT16", data[18], data[19]) * 0.001
        pib.cell11_voltage = convert_bytes_to_data("UINT16", data[20], data[21]) * 0.001
        pib.cell12_voltage = convert_bytes_to_data("UINT16", data[22], data[23]) * 0.001
        pib.cell13_voltage = convert_bytes_to_data("UINT16", data[24], data[25]) * 0.001
        pib.cell14_voltage = convert_bytes_to_data("UINT16", data[26], data[27]) * 0.001
        pib.cell15_voltage = convert_bytes_to_data("UINT16", data[28], data[29]) * 0.001
        pib.cell16_voltage = convert_bytes_to_data("UINT16", data[30], data[31]) * 0.001

        # Températures cellules (registres 0x1110 à 0x1113)
        pib.cell_temperature_1 = convert_bytes_to_data("UINT16", data[32], data[33]) * 0.1 - 273.15
        pib.cell_temperature_2 = convert_bytes_to_data("UINT16", data[34], data[35]) * 0.1 - 273.15
        pib.cell_temperature_3 = convert_bytes_to_data("UINT16", data[36], data[37]) * 0.1 - 273.15
        pib.cell_temperature_4 = convert_bytes_to_data("UINT16", data[38], data[39]) * 0.1 - 273.15

        # Registres 0x1114–0x1117 : réservés (bytes 40-47 ignorés)

        # Température environnement (registre 0x1118)
        if len(data) >= 50:
            pib.environment_temperature = convert_bytes_to_data("UINT16", data[48], data[49]) * 0.1 - 273.15

        # Température puissance (registre 0x1119)
        if len(data) >= 52:
            pib.power_temperature = convert_bytes_to_data("UINT16", data[50], data[51]) * 0.1 - 273.15

    except IndexError as e:
        _LOGGER.error("decode_pib_table: index error during decoding: %s", e)
        return None

    _LOGGER.debug("PIB decoded: %s", pib)
    return pib


# ---------------------------------------------------------------------------
# Point d'entrée principal
# ---------------------------------------------------------------------------

def extract_data_from_message(msg, telemetry_requested=True, teledata_requested=True,
                               debug=True, config_battery_address=None):
    """
    Parse les réponses Modbus (PIA + PIB) et retourne les données structurées.

    Args:
        msg:                    Liste de 2 trames hex (réponse PIA, réponse PIB)
        telemetry_requested:    Inutilisé pour l'instant (héritage)
        teledata_requested:     Inutilisé pour l'instant (héritage)
        debug:                  Inutilisé pour l'instant (héritage)
        config_battery_address: Adresse configurée (int ou str), utilisée comme libellé

    Returns:
        Tuple (battery_address, pia_data, pib_data, [], [])
        battery_address : str représentant l'adresse (ex: "0x01")
        pia_data        : instance V3PIATableData ou None si erreur
        pib_data        : instance V3PIBTableData ou None si erreur
    """
    # Normalisation de l'adresse pour l'affichage
    if isinstance(config_battery_address, int):
        address_string = f"0x{config_battery_address:02X}"
    else:
        address_string = str(config_battery_address) if config_battery_address else "unknown"

    pia_data = None
    pib_data = None

    if not msg or len(msg) < 2:
        _LOGGER.error("extract_data_from_message: msg must contain at least 2 frames")
        return address_string, pia_data, pib_data, [], []

    for idx, response in enumerate(msg):
        # Retirer le préfixe '~' si présent
        if isinstance(response, str) and response.startswith("~"):
            response = response[1:]

        _LOGGER.debug("Frame %d received: %s", idx, response)

        if idx == 0:
            pia_data = decode_pia_table(response)
            if pia_data is None:
                _LOGGER.error("PIA decoding failed for battery %s", address_string)
            else:
                _LOGGER.debug("PIA OK: %s", pia_data)

        elif idx == 1:
            pib_data = decode_pib_table(response)
            if pib_data is None:
                _LOGGER.error("PIB decoding failed for battery %s", address_string)
            else:
                _LOGGER.debug("PIB OK: %s", pib_data)

    return address_string, pia_data, pib_data, [], []
