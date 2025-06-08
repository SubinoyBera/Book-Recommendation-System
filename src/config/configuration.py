import os
import sys
from src.logger import logging
from src.exception import AppException
from src.utils import read_yaml, create_directories
from constants import *
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig

class AppConfiguration:
    def __init__(self, config_filepath: str = CONFIG_FILE_PATH):
        """
        Initializes the configuration object by reading configuration from config.yaml file..

        Parameters:
        config_filepath (str): Path to the configuration file.
        """
        try:
            self.config = read_yaml(config_filepath)
        except Exception as e:
            error_message = f"Failed to load configuration: {e}"
            raise AppException(Exception(error_message), sys)

    
    def data_ingestion_config(self) -> DataIngestionConfig:   
        """
        Creates the configuration for Data Ingestion 
        Returns: DataIngestionConfig object
        """
        try:
            ingestion_config = self.config.data_ingestion
            create_directories([ingestion_config.root_dir])

            ingestion_root_dir = ingestion_config.root_dir
            ingestion_dir = ingestion_config.ingestion_dir
            raw_data_dir = ingestion_config.raw_data_dir

            raw_data_dir = os.path.join(ingestion_root_dir, raw_data_dir)
            ingestion_data_dir = os.path.join(ingestion_root_dir, ingestion_dir)

            configuration = DataIngestionConfig(
                data_download_url = ingestion_config.data_download_url,
                raw_data_dir = raw_data_dir,
                ingested_dir = ingestion_data_dir
            )

            logging.info(f"Data Ingestion Configuration successfull")
            return configuration

        except Exception as e:
            error_message = f"Error in Data Ingestion Configuration: {e}"
            raise AppException(Exception(error_message), sys)


    def data_validation_config(self) -> DataValidationConfig:
        try:
            validation_config = self.config.data_validation
            ingestion_config = self.config.data_ingestion
            create_directories([validation_config.root_dir])

            validation_root_dir = validation_config.root_dir
            clean_data_dir = validation_config.clean_data_dir
            serialized_obj_dir = validation_config.serialized_obj_dir

            books_csvfile_dir = os.path.join(ingestion_config.root_dir, ingestion_config.ingested_data)
            ratings_csvfile_dir = os.path.join(ingestion_config.root_dir, ingestion_config.ingested_data)
            clean_data_path = os.path.join(validation_root_dir, clean_data_dir)
            serialized_obj_dir = os.path.join(validation_root_dir, serialized_obj_dir)

            configuration = DataValidationConfig(
                clean_data_dir = clean_data_path,
                books_csvfile = books_csvfile_dir,
                ratings_csvfile = ratings_csvfile_dir,
                serialized_objects_dir = serialized_obj_dir
            )

            logging.info(f"Data Validation process Configuration successfull")
            return configuration

        except Exception as e:
            error_message = f"Error in Data Validation process Configuration: {e}"
            raise AppException(Exception(error_message), sys)