import sys
from src.logger import logging
from src.exception import AppException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation

class MLPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
    
    def main(self):
        try:
            logging.info("STAGE:1 Data ingestion stage initiated")
            self.data_ingestion.initiate_data_ingestion()

            logging.info("STAGE:2 Data validation stage initiated")
            self.data_validation.initiate_data_vatidation()

            logging.info("STAGE:3 Data validation stage initiated")
            self.data_transformation.initiate_data_transformation()
        
        except Exception as e:
            logging.error(f"ML Pipeline Terminated: {e}", exc_info=True)
            raise AppException(e, sys)
        
if __name__=='__main__':
    try:
        logging.info("Starting ML Pipeline")
        obj = MLPipeline()
        obj.main()
        logging.info("ML Pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"ML pipeline terminated: {e}")
        raise AppException(e, sys)