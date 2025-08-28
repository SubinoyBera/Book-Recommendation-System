import os
import sys
import yaml
from src.core.logger import logging
from src.core.exception import AppException
from box import ConfigBox
from ensure import ensure_annotations
from pathlib import Path

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a YAML file and returns the content as a ConfigBox object.
    
    Args:
        path_to_yaml (Path): Path to the YAML file to be read.
    
    Returns:
        YAML file content as a ConfigBox object.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"yaml file: {path_to_yaml} loaded successfully.")
            
            return ConfigBox(content)
        
    except Exception as e:
        logging.error(f"Failed to read YAML file at {path_to_yaml}: {e}")
        raise AppException(e, sys)

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """
    Creates directories specified in the given list of paths.
    Args:
        path_to_directories (list): List of directory paths to be created.
        verbose (bool, optional): If True, logs the creation of each directory. Defaults to True.
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logging.info(f"Created directory: {path}")

    except Exception as e:
        logging.error("Failed to create directory at {path}: {e}")
        raise AppException(e, sys)