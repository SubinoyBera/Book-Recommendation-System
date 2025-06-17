import sys
import html
import pickle
import pandas as pd
from pathlib import Path
from src.logger import logging
from src.exception import AppException
from src.utils import create_directories
from src.config.configuration import AppConfiguration

class DataTransformation:
    def __init__(self, config = AppConfiguration()):
        """
        Initializes the DataValidation object.
        Args:
            app_config (AppConfiguration): The configuration object containing the configuration 
            for data validation.
        """
        try:
            logging.info(f"{'='*20}Data Transformation log started.{'='*20}")
            self.data_transformation_config = config.data_transformation_config

        except Exception as e:
            logging.error(f"Data validation Configuration initialization error: {e}", exc_info=True)
            raise AppException(e, sys)
        

    def transform(self):
        """
        Transforms the data by cleaning book titles, filtering users and books based on rating count, 
        and creating a pivot table for book recommendations.

        The function performs the following operations:
        - Reads the books and ratings data from configured file paths.
        - Cleans the book titles by removing escape characters and quotes.
        - Merges the books and ratings data on ISBN.
        - Filters users who have rated at least 200 books.
        - Filters books that have received at least 50 ratings.
        - Creates a pivot table with book titles as rows and user IDs as columns, 
          with ratings as values.
        - Saves the transformed pivot table, book names, and final ratings as pickle files.

        Raises:
            AppException: If any operation during data transformation or saving fails.
        """
        try:
            logging.info("Data Transformation operation started")
            books = pd.read_csv(self.data_transformation_config.books_data_path, sep=";", encoding="iso8859", on_bad_lines="skip")
            ratings = pd.read_csv(self.data_transformation_config.ratings_data_path, sep=";", encoding="iso8859", on_bad_lines="skip")

            books["Title"] = books["Title"].apply(html.unescape)
            books['Title'] = books["Title"].str.replace(r"\\'", "'", regex=True)
            books['Title'] = books["Title"].str.replace(r'\\"', '', regex=True)
            books['Title'] = books["Title"].str.replace(r'"', "", regex=True)
            books['Title'] = books["Title"].str.replace(r"\\", "", regex=True)

            df = ratings.merge(books, on="ISBN")

            # Get users who have rated min 200 books
            user_rating_df = df.groupby("user_id").count()
            x = user_rating_df["rating"]>=200
            good_users = x[x].index

            filtered_ratings = df[df["user_id"].isin(good_users)]

            # Get books that has received a total of min 50 ratings
            y = filtered_ratings.groupby("Title").count()["rating"]>=50
            good_books = y[y].index

            final_ratings = filtered_ratings[filtered_ratings["Title"].isin(good_books)]

            # create the pivot table
            books_pt = final_ratings.pivot_table(index="Title", columns="user_id", values="rating")
            books_pt.fillna(0, inplace=True)
            book_names = books_pt.index

            try:
                logging.info("Saving the transformed objects as pickle file")
                pickle.dump(books_pt, open(self.data_transformation_config.transformation_root/"books_pivot_table.pkl", "wb"))
                pickle.dump(book_names, open(self.data_transformation_config.transformation_root/"book_names.pkl", "wb"))
                pickle.dump(final_ratings, open(self.data_transformation_config.transformation_root/"final_ratings.pkl", "wb"))

            except Exception as e:
                logging.error(f"Failed to save the transformed objects: {e}", exc_info=True)
                raise AppException(e, sys)
            
        except Exception as e:
            logging.error(f"Data Transformation operation failed: {e}", exc_info=True)
            raise AppException(e, sys)


    def initiate_data_transformation(self):
        """
        Starts the data transformation process.

        - Transforms the data by cleaning book titles
        - Filtering users and books based on rating count 
        - Creates pivot table for book recommendations
        - Saves the transformed objects
        - Raises: AppException If any operation during data transformation or saving fails
        """
        try:
            self.transform()
            logging.info(f"{'='*20}Data Transformation Completed Successfully.{'='*20} \n\n")
        
        except Exception as e:
            logging.error(f"Dataset Transformation error: {e}", exc_info=True)
            raise AppException(e, sys)