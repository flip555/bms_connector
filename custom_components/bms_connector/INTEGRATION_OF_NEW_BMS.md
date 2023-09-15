## How to Add a New BMS Type/Version/Manufacturer to the Repository

Follow the steps below:

### 1. **Create BMS Folder**:
   
   If there's no appropriate folder for the BMS manufacturer in the `bms/` directory:
   - Create one using the structure:
     ```
     bms/manufacturer_of_bms/version_ref/
     ```
   - Replace `manufacturer_of_bms` with the actual manufacturer's name and `version_ref` with the BMS version or reference.

### 2. **Edit .const.py**:

   In the `.const.py` file:
   - Add an entry for your BMS type under the `BMS_TYPES` dictionary. For instance:
     ```python
     BMS_TYPES = {
         "SEPLV2": "SEP BMS V2 (SEPLV2)",
         "SEPLV3": "SEP BMS V3 (SEPLV3)",
         "YOURBMS": "Your BMS Description",
     }
     ```
   - Replace "YOURBMS" with your BMS type's identifier and give it a descriptive name.

### 3. **Edit .sensor.py**:

   In the `.sensor.py` file:
   - Add the necessary import for your BMS routing.
   - Find the "BMS Routing Imports" section and include imports for your BMS type's sensor generation. For example:
     ```python
     #################################################
     ############## BMS Routing Imports ##############
     #################################################
     from .bms.seplos.v2.sensors import generate_sensors as SEPLOS_V2_START
     from .bms.seplos.v3.sensors import generate_sensors as SEPLOS_V3_START
     from .bms.manufacturer_of_bms.version_ref.sensors import generate_sensors as YOURBMS_START
     ```
   - Replace `manufacturer_of_bms` and `version_ref` with the manufacturer and version/reference names respectively. Also, add an import for your BMS type, using the identifier from step 2.

### 4. **Add Logic Step**:

   Inside the `.sensor.py` file:
   - Find the BMS routing section and introduce a logic step for your BMS type. For instance:
     ```python
     # For Your BMS
     elif bms_type == "YOURBMS":
         _LOGGER.debug("%s selected. Routing now..", bms_type)
         await YOURBMS_START(hass, bms_type, port, battery_address, sensor_prefix, entry, async_add_entities)
     ```
   - Replace "YOURBMS" with the identifier from step 2.

### 5. **Add BMS Sensors**:

   - Make a new file titled `sensors.py` in the directory you made in step 1 (`bms/manufacturer_of_bms/version_ref/`).
   - Implement the sensor generation logic for your BMS type in this file.

### 6. **Submit a Pull Request**:

   Once you've added the necessary files and logic for your BMS type:
   - Submit a pull request on GitHub for evaluation and merging into the repository.
   - Make sure to include clear documentation and comments on your changes to ease the review.

By adhering to these steps, you can contribute a new BMS type/version/manufacturer to the repository.