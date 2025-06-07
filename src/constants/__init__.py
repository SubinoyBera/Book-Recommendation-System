# Constants for configuration file paths
# This module defines constants for the configuration file paths used in the application.
import os

ROOT_DIR = os.getcwd()
# Main configuration file path
CONFIG_FOLDER_NAME = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_FOLDER_NAME, CONFIG_FILE_NAME)