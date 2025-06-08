# Constants for configuration file paths
# This module defines constants for the configuration file paths used in the application.

import os

# Get current working directory
ROOT_DIR = os.getcwd()

# Main configuration file path
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_FILE_NAME)

# Schema file path
SCHEMA_FILE_NAME = "schema.yaml"
SCHEMA_FILE_PATH = os.path.join(ROOT_DIR, SCHEMA_FILE_NAME)