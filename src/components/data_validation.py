import os
import sys
from pathlib import Path
import pandas as pd
from src.logger import logging
from src.exception import AppException
from src.utils import create_directories
from src.config.configuration import AppConfiguration

def get_validation(columns, schema):
    """
    Validates the given columns against the given schema.
    Args:
        columns (list): Columns to be validated.
        schema (dict): Schema used for the columns validation.
        
    Returns:
        bool: True if all columns are present in the schema, False otherwise.
    """
    for col in columns:
        if col not in schema:
            validation_status = False
        else:
            validation_status = True

    return validation_status


class DataValidation:
    def __init__(self, app_config = AppConfiguration()):
        """
        Initializes the DataValidation object.
        Args:
            app_config (AppConfiguration): The configuration object containing the configuration 
            for data validation.
        """
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.data_validation_config = app_config.data_validation_config()

        except Exception as e:
            logging.error(f"Data validation Configuration initialization error: {e}")
            raise AppException(e, sys)


    def validate_dataset(self):
        """
        Validates the ingested datasets.

        This method reads the ingested datasets, processes and validates them 
        according to the given schema. If the validation is successful, it writes 
        the validation status to a status file and saves the validated datasets to a specific directory.

        Returns: None
        """
        try:
            logging.info("Reading ingested datasets")
            books = pd.read_csv(self.data_validation_config.books_csvfile, sep=";", encoding="iso8859", on_bad_lines="skip")
            ratings = pd.read_csv(self.data_validation_config.ratings_csvfile, sep=";", encoding="iso8859", on_bad_lines="skip")
            
            logging.info("Processing datasets for validation")
            books.drop(['Image-URL-S', 'Image-URL-M'], axis=1, inplace=True)
            books.rename(columns = {"Book-Title" : "Title",
                                    "Book-Author" : "Author",
                                    "Year-Of-Publication" : "Year",
                                    "Image-URL-L" : "image_url"}, inplace=True)
            
            ratings.rename(columns = {"User-ID" : "user_id",
                                      "Book-Rating" : "rating"}, inplace=True)

            books_cols = list(books.columns)
            ratings_cols = list(ratings.columns)
            book_schema = self.data_validation_config.book_schema.keys()
            ratings_schema = self.data_validation_config.ratings_schema.keys()

            book_validation_status = get_validation(books_cols, book_schema)
            ratings_validation_status = get_validation(ratings_cols, ratings_schema)

            try:
                if book_validation_status & ratings_validation_status == True:
                    with open(self.data_validation_config.STATUS_FILE, 'w') as f:
                       f.write(f"Validation Status: True")

                    logging.info("Datasets successsfully validated")
                    create_directories(self.data_validation_config.valid_data_dir)
                    valid_books_dataset = "valid_books_dataset.csv"
                    valid_ratings_dataset = "valid_books_dataset.csv"

                    books.to_csv(Path(self.data_validation_config.valid_data_dir/valid_books_dataset), index=False)
                    ratings.to_csv(Path(self.data_validation_config.valid_data_dir/valid_ratings_dataset), index=False)
                    logging.info(f"Validated dataset saved at {self.data_validation_config.valid_data_dir}")

            except Exception as e:
                if book_validation_status == False:
                    logging.error(f"Books dataset validation failed: {e}")
                    raise AppException(e, sys)
                else:
                    logging.error(f"Ratings dataset validation failed: {e}")
                    raise AppException(e, sys)
            
        except Exception as e:
            logging.error(f"Dataset validation process failed: {e}")
            raise AppException(e, sys)


    def initiate_data_vatidation(self):
        """
        This function starts the data validation process
        - Validates the dataset and writes the valid dataset to a specified location
        - Logs the validation status
        - Raises an exception if the validation fails
        """
        try:
            self.validate_dataset()
            logging.info(f"{'='*20}Data Validation Completed Successfully.{'='*20} \n\n")
        
        except Exception as e:
            logging.error(f"Dataset Validation error: {e}")
            raise AppException(e, sys)