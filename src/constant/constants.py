# Constants for configuration file paths
# This module defines constants for the configuration file paths used in the application.

import os
from pathlib import Path

# Get current working directory
ROOT_DIR = os.getcwd()

# Main path configuration folder
CONFIG_FOLDER = "config"

# Config file path
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = Path(ROOT_DIR, CONFIG_FOLDER, CONFIG_FILE_NAME)

# Schema file path
SCHEMA_FILE_NAME = "schema.yaml"
SCHEMA_FILE_PATH = Path(ROOT_DIR, CONFIG_FOLDER, SCHEMA_FILE_NAME)