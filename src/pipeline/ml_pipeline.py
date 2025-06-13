import sys
from src.logger import logging
from src.exception import AppException
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

class MLPipeline:
    def __init__(self):
        """
        Initializes the components of the ML Pipeline
        """
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.data_transformation = DataTransformation()
        self.model_trainer = ModelTrainer()
    
    def main(self):
        """
        Initiates the Machine Learning Pipeline which involves stages like Data Ingestion, Data Validation, Data Transformation and Model Training.

        Raises:
            AppException: If any stage of the pipeline fails
        """
        try:
            logging.info("STAGE:1 Data Ingestion Stage Initiated")
            self.data_ingestion.initiate_data_ingestion()

            logging.info("STAGE:2 Data Validation Stage Initiated")
            self.data_validation.initiate_data_vatidation()

            logging.info("STAGE:3 Data Transformation Stage Initiated")
            self.data_transformation.initiate_data_transformation()

            logging.info("STAGE:3 Model Training Stage Initiated")
            self.model_trainer.initiate_training()
        
        except Exception as e:
            logging.error(f"ML Pipeline Terminated: {e}", exc_info=True)
            raise AppException(e, sys)
        
if __name__=='__main__':
    try:
        logging.info("ML Pipeline started")
        obj = MLPipeline()
        obj.main()
        logging.info("ML Pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"ML pipeline terminated: {e}", exc_info=True)
        raise AppException(e, sys)