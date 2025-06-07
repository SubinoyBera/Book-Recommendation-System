import os
import sys
import requests
import zipfile
from src.logger import logging
from src.exception import AppException
from src.utils import create_directories
from src.config.configuration import AppConfiguration

class DataIngestion:
    def __init__(self, app_config = AppConfiguration()):
        """
        DataIngestion Intialization
        data_ingestion_config: DataIngestionConfig 
        """
        try:
            logging.info(f"{'='*20}Data Ingestion log started.{'='*20} ")
            self.data_ingestion_config= app_config.data_ingestion_config()

        except Exception as e:
            error_message = f"Data Ingestion error: {e}"
            raise AppException(Exception(error_message), sys)

    
    def download_data(self):
        """
        Downloads data from the given url and saves it into a zip file into the given location.

        Returns:
            str: The path of the downloaded zip file
        """
        try:
            dataset_url = self.data_ingestion_config.data_download_url
            zip_download_dir = self.data_ingestion_config.raw_data_dir
            create_directories(zip_download_dir)

            data_filename = os.path.basename(dataset_url)
            zip_file_path = os.path.join(zip_download_dir, data_filename)

            logging.info(f"Downloading data from {dataset_url}")
            response = requests.get(dataset_url)
            if response.status_code == 200:
                with open(zip_file_path, "wb") as f:
                    f.write(response.content)
                    logging.info(f"Downloaded data successfully into file: {zip_file_path}")

            return zip_file_path

        except Exception as e:
            error_message = f"Failed to download data: {e}"
            raise AppException(Exception(error_message), sys)


    def extract_zip_file(self,zip_file_path: str):
        """
        Extracts the given zip file into a given directory.
        Args:
            zip_file_path (str): The path of the zip file to be extracted
        """
        try:
            ingested_dir = self.data_ingestion_config.ingested_dir
            create_directories(ingested_dir)

            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(ingested_dir)
            logging.info(f"Extracting zip file: {zip_file_path} into dir: {ingested_dir}")

        except Exception as e:
            error_message = f"Failed to extract Zip file: {e}"
            raise AppException(Exception(error_message), sys)


    def initiate_data_ingestion(self):
        """
        Starts the data ingestion process by downloading the data from given url and saving it into a given location. 
        Extracts the given zip file into a given directory.

        Raises:
            AppException: If error occurs during data ingestion
        """
        try:
            zip_file_path = self.download_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            logging.info(f"{'='*20}Data Ingestion Completed Successfully.{'='*20} \n\n")
        
        except Exception as e:
            error_message = f"Error in Data Ingestion process: {e}"
            raise AppException(Exception(error_message), sys)