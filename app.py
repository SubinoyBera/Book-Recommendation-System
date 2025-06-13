import os
import sys
import pickle
import numpy as np
import streamlit as st
from src.config.configuration import AppConfiguration
from src.pipeline import ml_pipeline
from src.logger import logging
from src.exception import AppException

class Recommendation:
    def __init__(self, app_config = AppConfiguration()):
        try:
            self.recommend_config = app_config.recommendation_config

            # if model is available load model
            self.model = pickle.load(open(self.recommend_config.trained_model_path, "rb"))
            self.final_ratings = pickle.load(open(self.recommend_config.final_ratings_obj_path, "rb"))
            self.books_pivot_table = pickle.load(open(self.recommend_config.books_pivot_table_obj_path, "rb"))

        except Exception as e:
            logging.error(f"Failed to initialize Recommendation Congiguration: {e}", exc_info=True)
            raise AppException(e, sys)
            

    def get_poster(self, suggestion):
        book_names = []
        ids_index = []
        poster_url = []
        try:
            for book_id in suggestion:
                book_names.append(self.books_pivot_table.index[book_id])

            for book in book_names[0]:
                ids = np.where(self.final_ratings["Title"] == book)[0][0]
                ids_index.append(ids)

            for id in ids_index:
                url = self.final_ratings.iloc[id]["image_url"]
                poster_url.append(url)

            return poster_url

        except Exception as e:
            logging.error(f"Failed to fetch poster image: {e}", exc_info=True)
            raise AppException(e, sys)


    def recommend(self, book_name):
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

            return books_list, poster_url

        except Exception as e:
            logging.error(f"Failed to get recommendations from the model: {e}", exc_info=True)
            raise AppException(e, sys)

    

if __name__ == "__main__":
    st.header("Book Recommender System")
    st.text("Collaborative filtering based recommendation system!")

    # create an object of recommendation class
    obj = Recommendation()

    if st.button("Train Recommender System"):
        # train recommender: obj.train_engine()
        pass

    book_names = pickle.load(open("path to book_names.pkl", "rb"))
    selected_book = st.selectbox(
        "Type or Select books from the dropdown...",
        book_names)

    if st.button("Show Recommendations"):
        # obj.recommand_engine(selected)
        pass
