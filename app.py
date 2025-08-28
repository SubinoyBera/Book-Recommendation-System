# Book Recommender System Application
import os
import sys
import pickle
import shutil
from pathlib import Path

import numpy as np
import streamlit as st
from src.core.configuration import AppConfiguration
from src.pipeline.ml_pipeline import MLPipeline
from src.core.logger import logging
from src.core.exception import AppException

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr
from dotenv import load_dotenv
load_dotenv()

class MLRecommender:
    def __init__(self, app_config = AppConfiguration()):        
        """
        Initializes the MLRecommendation object.
        Args:
            app_config (AppConfiguration): The configuration object containing the ml-recommendation settings.

        Loads the trained model, final ratings, and books pivot table if the trained model path exists.
        """
        try:
            self.ml_recommend_config = app_config.ml_recommendation_config()

            # check if ml model and serialized objects is available then load
            if os.path.exists(self.ml_recommend_config.trained_model_path) & os.path.exists(self.ml_recommend_config.serialized_obj_dir):
                self.model = pickle.load(open(self.ml_recommend_config.trained_model_path, "rb"))
                self.final_ratings = pickle.load(open(self.ml_recommend_config.final_ratings_obj_path, "rb"))
                self.books_pivot_table = pickle.load(open(self.ml_recommend_config.books_pivot_table_obj_path, "rb"))

                self.obj_loaded = True

            else:
                self.obj_loaded = False

        except Exception as e:
            logging.error(f"Failed to initialize Recommendation Congiguration: {e}", exc_info=True)
            raise AppException(e, sys)
            

    def train_engine(self):
        """
        This method is used to train the recommendation model.
        It initializes the ML pipeline and trains the model.
        """
        dirs = ["artifacts/data_ingestion", "artifacts/data_validation", "artifacts/data_transformation",
                    "artifacts/serialized_objects", "artifacts/common_objects", "artifacts/ML_model"]
        for dir in dirs:
            if os.path.exists(Path(dir)):
                shutil.rmtree(dir)

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
                if type(url) is float:
                    logging.warning(f"No poster url found for book ID {id}, using default image")
                    url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgVr8P6ExMHCBQEiGITlb89tDlY878ROSfQH-JVVdCTJNHCk9EjKESYuy6-R2x9Qg3ptw&usqp=CAU"
                    
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

    
    def ml_recommendation_engine(self,selected_book):
        """
        Displays the recommended books and their poster images based on a selected book.
        This method uses the `recommend` method to get recommendations and then displays them in a Streamlit app.

        Args:
            selected_book (str): The name of the book for which recommendations are needed.
        """
        try:
            logging.info("ML-Recommender Engine Started.")
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
            logging.info("Recommender Engine successfully provided recommendations.")

        except Exception as e:
            logging.error(f"ML Recommendation engine failure: {e}", exc_info=True)
            raise AppException(e, sys)


class SemanticRecommender:
    def __init__(self, app_config = AppConfiguration()):        
        """
        Initializes the SemanticRecommender object.
        Loads the pre-computed Chroma vector store and the final books data object. 
        Also loads the Google Generative AI embeddings model.

        Args:
            app_config (AppConfiguration): The configuration object containing the configuration for semantic recommendation.
        """
        try:
            api_key = os.getenv("GOOGLE_API_KEY")

            self.embedding = GoogleGenerativeAIEmbeddings(model = "models/text-embedding-004",
                                                    google_api_key = SecretStr(api_key) if api_key is not None else None)

            recommend_config = app_config.semantic_recommender_config()

            self.books_data = pickle.load(open(recommend_config.final_books_obj_path, "rb"))
            self.chroma_persist_dir = recommend_config.chroma_persist_dir

        except Exception as e:
            logging.error(f"Semantic Recommender class initialization failed: {e}", exc_info=True)
            raise AppException(e, sys)
        
    
    def semmantic_recommend(self, query):
        """
        Performs a semantic search for relevant books based on description provided.
        Args:
            query (str): The search query describing the type of books to find.

        Returns:
            tuple: A tuple containing:
                - books (list): A list of book titles that match the query.
                - posters_url (list): A list of URLs for the poster images of the matching books.
        """
        book_ids = []
        books = []
        posters_url = []
        
        logging.info(f"Searching for books based on semantics of the description provided.")
        try:
            db_books = Chroma(persist_directory = str(self.chroma_persist_dir),
                              embedding_function = self.embedding)

            results = db_books.similarity_search(query, k=8)

            for i, doc in enumerate(results, 1):
                book_ids.append(doc.page_content.split()[0].replace(':', '').strip())

            for i in book_ids:
                if i[0] == '"':
                    i = i.replace('"', '')
                id_int = int(i)
                index = np.where(self.books_data["isbn13"] == id_int)[0][0]
                title = self.books_data["title"].iloc[index]
                books.append(title)

                thumbnail_url = self.books_data["thumbnail"].iloc[index]
                if type(thumbnail_url) is float:
                        logging.warning(f"No poster url found for book ID {index}, using default image")
                        thumbnail_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgVr8P6ExMHCBQEiGITlb89tDlY878ROSfQH-JVVdCTJNHCk9EjKESYuy6-R2x9Qg3ptw&usqp=CAU"

                posters_url.append(thumbnail_url)

            logging.info(f"Recommended books and poster image urls fetched successfully.")
            return books, posters_url
        
        except Exception as e:
            logging.error(f"Embedding model failed to recommend books and or couldn't get poster image urls: {e}", exc_info=True)
            raise AppException(e, sys)
    

    def semantic_recommendation_engine(self, book_desc):
        """
        Displays the recommended books and their poster images based on a given book description.
        This method uses the `semantic_recommend` method to get recommendations and then displays them in a Streamlit app.

        Args:
            book_desc (str): The description of the book for which recommendations are needed.
        """
        try:
            logging.info("Semantic Recommender Engine Started.")
            recommended_books, poster_urls = self.semmantic_recommend(book_desc)
            
            for i in range(0, len(poster_urls), 4):
                cols = st.columns(4)
                for j in range(4):
                    if i+j < len(poster_urls):
                        with cols[j]:
                            st.image(poster_urls[i+j])
                            st.markdown(f"**{recommended_books[i+j]}**")
            
            logging.info("Recommender Engine successfully provided recommendations.")

        except Exception as e:
            logging.error(f"Semantic Recommendation engine failure: {e}", exc_info=True)
            raise AppException(e, sys)


# Book Recommender System Application using Streamlit
# This application provides a user interface for book recommendations using either a Machine Learning or Semantic approach.
if __name__ == "__main__":
    st.set_page_config(page_title = "Book Recommendation System", layout = "wide", page_icon=":books:")
    
    # Set sidebar title and options
    st.sidebar.title("Options ~")
    option = st.sidebar.selectbox("Please Choose Recommender Type :",
                            ["ML Recommender",
                             "Semantic Recommender"]
    )

    for _ in range(23):
        st.sidebar.write("")

    st.sidebar.markdown("**--->>> Developed and Engineered by SUBINOY BERA**")
    st.sidebar.markdown("Thank You!! 😀🙏")
    
    # ML Recommender System
    if option == "ML Recommender":
        st.header("ML Book Recommender System 📚📖")
        st.text("--  🔖 Collaborative Filtering based End to End Machine Learning book recommendation system!!")

        obj = MLRecommender()

        if st.button("Train Recommender System"):
            try:
                with st.spinner("🛠️ Training in Progress ..."):
                    obj.train_engine()
                    st.success("🎉 Recommender System Successfully Trained!!")

            except Exception as e:
                st.error("Failed to train Recommender System! Error occured during training. Please reload application and try again ...")
                logging.error(f"Recommender System training error: {e}")
                raise AppException(e, sys)


        book_names_obj_path = obj.ml_recommend_config.book_names_obj_path
        if not os.path.exists(book_names_obj_path):
            st.error("Required file objects not found. Please retrain the Recommender System.")
        else:
            book_names = pickle.load(open(book_names_obj_path, "rb"))
        
            selected_book = st.selectbox("Type or Select book from the dropdown to get recommendation :",
                                    book_names)

        if st.button("Show Recommendations"):
            if not obj.obj_loaded:
                st.error("Sorry!! No Recommendation Model found and or other required file objects not found. Please train the Recommender System.")
            else:
                try:
                    obj.ml_recommendation_engine(selected_book)

                except Exception  as e:
                    st.error("Unexpected Error occureed :( ")
                    logging.error(f"Ml recommendation engine failure: {e}")
                    raise AppException(e, sys)

    # Semantic Recommender System
    if option == "Semantic Recommender":
        st.header("Semantic Book Recommender System 📔🧩")
        st.text("--  ⚙️ Uses Google Embedding model and Vector Similarity Search to give book recommendations based on the description!!")

        book_desc = st.text_input("Please write book description...")

        if st.button("Show Recommendations"):
            if not book_desc:
                st.error("Sorry! Please write a book description in the input-box to provide recommendations.")
            else:
                try:
                    obj = SemanticRecommender()
                    obj.semantic_recommendation_engine(book_desc)

                except Exception  as e:
                    st.error("Unexpected Error occureed :( ")
                    logging.error(f"Semantic recommendation engine failure: {e}")
                    raise AppException(e, sys)