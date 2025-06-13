import sys
import pickle
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from src.logger import logging
from src.exception import AppException
from src.config.configuration import AppConfiguration

class ModelTrainer:
    def __init__(self, app_config = AppConfiguration()):
        """
        Initializes the ModelTrainer object.
        Args:
            app_config (AppConfiguration): The configuration object containing the configuration 
            for model training.
        """
        try:
            logging.info(f"{'='*20}Model Trainer log started.{'='*20}")
            self.model_trainer_config = app_config.model_trainer_config()

        except Exception as e:
            logging.error(f"Model Trainer configuration initialization error: {e}", exc_info=True)
            raise AppException(e, sys)


    def train(self):
        """
        Trains NearestNeighbors model using the pre-processed book pivot table.

        Loads the book pivot table, converts it into a Compressed Sparse Row (CSR) matrix, and trains a NearestNeighbors model using the 'brute' algorithm. 
        The trained model is then saved to a specified directory.

        Raises:
            AppException: If model training process or saving model fails
        """
        try:
            logging.info("Starting model training")
            # load the pivot table
            books_pivot_table = pickle.load(open(self.model_trainer_config.books_pivot_table_path, "rb"))
            # convert to csr matrix
            books_sparse = csr_matrix(books_pivot_table)
            
            # training model
            model = NearestNeighbors(algorithm = "brute")
            model.fit(books_sparse)

            # save the trained model
            model_name = self.model_trainer_config.model_name
            pickle.dump(model, open(self.model_trainer_config.trained_model_dir/model_name, "wb"))
            logging.info(f"Model succesfully trained and saved")

        except Exception as e:
            logging.error(f"Model training terminated: {e}", exc_info=True)
            raise AppException(e, sys)
            

    def initiate_training(self):
        """
        This method starts the model training by calling the train method.

        Raises
        ------
        AppException
            If any exception occurs during model training
        """
        try:
            self.train()
            logging.info(f"{'='*20}Model Training Successfully.{'='*20} \n\n")

        except Exception as e:
            logging.error(f"Model training failed: {e}", exc_info=True)
            raise AppException(e, sys)