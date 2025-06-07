import sys
from src.logger import logging
from src.exception import AppException
from src.components.data_ingestion import DataIngestion

class DataIngestionPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
    
    def main(self):
        self.data_ingestion.initiate_data_ingestion()
        
if __name__=='__main__':
    try:
        logging.info("Starting data ingestion pipeline")
        obj= DataIngestionPipeline()
        obj.main()
        logging.info("Data ingestion pipeline ended.")
        
    except Exception as e:
        error_message = f"Data ingestion pipeline terminated: {e}"
        raise AppException(Exception(error_message), sys)