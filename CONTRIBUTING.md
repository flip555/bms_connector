# Contributing Guidelines

Thank you for your interest in contributing to our project! Whether you're reporting bugs, proposing new features, or contributing code, we appreciate your support. Here are some guidelines to follow:

## Git Branch Workflow

### Main Branch

- **Branch name**: `main`
- **Purpose**: This branch contains the production-ready code. It should always be stable and deployable.
- **Maintainer**: flip555

### Next Branch

- **Branch name**: `next-branch`
- **Purpose**: This is the development or integration branch where new features and fixes are accumulated before being merged into `main`.
- **Maintainer**: flip555

### Feature or Fix Branches

- **Branch names**: E.g., `battery-multipacks`
- **Purpose**: These branches are created for new features or fixes to keep work isolated. They will be merged into `next-branch` once completed.
- **Maintainer**: Individual contributors

### Workflow Overview

1. **Creating new branches**: For any new feature or fix, create a new branch.
2. **Merging into `next-branch`**: Once your work is complete, create a pull request to merge it into `next-branch`.
3. **Testing**: Before merging changes into `main`, we conduct thorough testing in the `next-branch`.
4. **Merging into `main`**: After ensuring stability, changes from `next-branch` are merged into `main`.
5. **Releasing**: Following a successful merge into `main`, tag the commit with a version number to indicate a new release.
6. **Reset `next-branch`**: Post-release, reset `next-branch` to the current state of `main` to begin the next development cycle.

## Getting Help

Feel free to use resources like ChatGPT to assist you, even if you are a novice coder. We are here to foster a collaborative and inclusive environment.

## Reporting Issues

When reporting issues, please be as descriptive as possible. Provide the steps to reproduce the issue, expected outcome, and actual results.

Thank you for your collaboration and contribution!

