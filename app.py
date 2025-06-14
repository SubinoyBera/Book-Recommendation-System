import os
import sys
import pickle
import numpy as np
import streamlit as st
from src.config.configuration import AppConfiguration
from src.pipeline.ml_pipeline import MLPipeline
from src.logger import logging
from src.exception import AppException

class Recommendation:
    def __init__(self, app_config = AppConfiguration()):        
        """
        Initializes the Recommendation object.
        Args:
            app_config (AppConfiguration): The configuration object containing the recommendation settings.

        Loads the trained model, final ratings, and books pivot table if the trained model path exists.
        """
        try:
            self.recommend_config = app_config.recommendation_config

            # check if ml model is available
            if self.recommend_config.trained_model_path.exists():
                self.model = pickle.load(open(self.recommend_config.trained_model_path, "rb"))
                self.final_ratings = pickle.load(open(self.recommend_config.final_ratings_obj_path, "rb"))
                self.books_pivot_table = pickle.load(open(self.recommend_config.books_pivot_table_obj_path, "rb"))

        except Exception as e:
            logging.error(f"Failed to initialize Recommendation Congiguration: {e}", exc_info=True)
            raise AppException(e, sys)
            

    def train_engine(self):
        """
        This method is used to train the recommendation model.
        It initializes the ML pipeline and trains the model.
        """
        try:
            logging.info("Training Recommender System Started")
            pipeline = MLPipeline()
            pipeline.main()
            logging.info("Recommender System successfully trained.")

        except Exception as e:
            logging.error(f"Failed to train recommender system: {e}", exc_info=True)
            raise AppException(e, sys)


    def get_poster(self, suggestion):
        """
        Fetches the poster URLs for a list of suggested books.
        Args:
            suggestion (list): A list of suggested book IDs.
        Returns:
            list: A list of URLs pointing to the poster images of the suggested books.
        """
        book_names = []
        ids_index = []
        poster_url = []
        try:
            logging.info("Fetching poster images for recommended books.")
            for book_id in suggestion:
                book_names.append(self.books_pivot_table.index[book_id])

            for book in book_names[0]:
                ids = np.where(self.final_ratings["Title"] == book)[0][0]
                ids_index.append(ids)

            for id in ids_index:
                url = self.final_ratings.iloc[id]["image_url"]
                if url is None or url == "nan":
                    logging.warning(f"No poster url found for book ID {id}")
                    url = "https://developers.google.com/static/maps/documentation/streetview/images/error-image-generic.png"
                    
                poster_url.append(url)
            
            logging.info("Poster images fetched successfully.")
            return poster_url

        except Exception as e:
            logging.error(f"Failed to fetch poster image: {e}", exc_info=True)
            raise AppException(e, sys)


    def recommend(self, book_name):
        """
        Recommends a list of books similar to the given book name.
        Args:
            book_name (str): The name of the book for which recommendations are needed.
        Returns:
            tuple: A tuple containing:
                - books_list (list): A list of recommended book titles.
                - poster_url (list): A list of URLs pointing to the poster images of the recommended books.
        """
        logging.info(f"Getting recommendations for the book: {book_name}")
        books_list = []
        try:
            book_id = np.where(self.books_pivot_table.index == book_name)[0][0]
            _ , suggestion = self.model.kneighbors(self.books_pivot_table.iloc[book_id,:].values.reshape(1,-1),
                                                    n_neighbors = 6)
            
            poster_url = self.get_poster(suggestion)

            for i in range(len(suggestion)):
                books = self.books_pivot_table.index[suggestion[i]]
                for j in books:
                    books_list.append(j)

            logging.info(f"Recommendations for {book_name} fetched successfully.")
            return books_list, poster_url

        except Exception as e:
            logging.error(f"Failed to get recommendations from the model: {e}", exc_info=True)
            raise AppException(e, sys)

    
    def recommendation_engine(self,selected_book):
        """
        Displays the recommended books and their poster images based on a selected book.
        This method uses the `recommend` method to get recommendations and then displays them in a Streamlit app.

        Args:
            selected_book (str): The name of the book for which recommendations are needed.
        """
        try:
            recommended_books, poster_url = self.recommend(selected_book)
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.image(poster_url[1])
                st.text(recommended_books[1])
            with col2:
                st.image(poster_url[2])
                st.text(recommended_books[2])
            with col3:
                st.image(poster_url[3])
                st.text(recommended_books[3])
            with col4:
                st.image(poster_url[4])
                st.text(recommended_books[4])
            with col5:
                st.image(poster_url[5])
                st.text(recommended_books[5])

        except Exception as e:
            logging.error(f"Recommendation engine failure: {e}", exc_info=True)
            raise AppException(e, sys)


# Streamlit application for the Book Recommender System
# This application allows users to train the recommender system and get book recommendations based on a selected book
if __name__ == "__main__":
    st.header("Book Recommender System")
    st.text("Collaborative filtering based recommendation system!")

    obj = Recommendation()

    if st.button("Train Recommender System"):
        obj.train_engine()

    book_names_obj_path = obj.recommend_config.book_names_obj_path
    book_names = pickle.load(open(book_names_obj_path, "rb"))
    selected_book = st.selectbox("Type or Select books from the dropdown...",
                                book_names)

    if st.button("Show Recommendations"):
        obj.recommendation_engine(selected_book)