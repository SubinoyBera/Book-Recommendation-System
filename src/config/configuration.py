# Configuration module for the Book Recommendation System
# This module handles the loading and management of configuration settings for data ingestion, validation, transformation, and model training.
import sys
from pathlib import Path
from src.logger import logging
from src.exception import AppException
from src.utils import read_yaml, create_directories
from src.constant.constants import *
from src.entity.config_entity import (DataIngestionConfig, DataValidationConfig, DataTransformationConfig, 
                                      ModelTrainerConfig, MLRecommendationConfig, SemanticRecommendationConfig)

class AppConfiguration:
    def __init__(self, 
                config_filepath : Path = CONFIG_FILE_PATH,
                config_schemapath : Path = SCHEMA_FILE_PATH):
        """
        Initializes the configuration object by reading configuration from config.yaml file..

        Parameters:
        config_filepath (str): Path to the configuration file.
        """
        try:
            self.config = read_yaml(config_filepath)
            self.schema = read_yaml(config_schemapath)

        except Exception as e:
            logging.error(f"Failed to load configuration: {e}", exc_info=True)
            raise AppException(e, sys)

    
    def data_ingestion_config(self) -> DataIngestionConfig:   
        """
        Creates the configuration for Data Ingestion 
        Returns: DataIngestionConfig object
        """
        try:
            ingestion_config = self.config.data_ingestion
            create_directories([ingestion_config.root_dir])

            ingestion_root_dir = ingestion_config.root_dir
            ingestion_dir = ingestion_config.ingestion_dir
            raw_data_dir = ingestion_config.raw_data_dir

            raw_data_dir = Path(ingestion_root_dir, raw_data_dir)
            ingestion_data_dir = Path(ingestion_root_dir, ingestion_dir)

            ingestion_configuration = DataIngestionConfig(
                data_download_url = ingestion_config.data_download_url,
                raw_data_dir = raw_data_dir,
                ingested_dir = ingestion_data_dir
            )

            logging.info("Data Ingestion Configuration creation successfull")
            return ingestion_configuration

        except Exception as e:
            logging.error(f"Error while creating Data Ingestion Configuration: {e}", exc_info=True)
            raise AppException(e, sys)


    def data_validation_config(self) -> DataValidationConfig:
        """
        Creates the configuration for Data Validation 
        Returns: DataValidationConfig object
        """
        try:
            validation_config = self.config.data_validation
            ingestion_config = self.config.data_ingestion
            book_schema = self.schema.BOOKS_COLUMNS
            ratings_schema = self.schema.RATINGS_COLUMNS

            create_directories([validation_config.root_dir])

            validation_root_dir = validation_config.root_dir
            valid_data_dir = validation_config.valid_data_dir
            books_csvfile = validation_config.books_csvfile
            ratings_csvfile = validation_config.ratings_csvfile

            books_csvfile_path = Path(ingestion_config.root_dir, ingestion_config.ingestion_dir, books_csvfile)
            ratings_csvfile_path = Path(ingestion_config.root_dir, ingestion_config.ingestion_dir, ratings_csvfile)
            valid_data_path = Path(validation_root_dir, valid_data_dir)
            
            STATUS_FILE_PATH = Path(validation_root_dir, validation_config.STATUS_FILE)

            validation_configuration = DataValidationConfig(
                valid_data_dir = valid_data_path,
                books_csvfile = books_csvfile_path,
                ratings_csvfile = ratings_csvfile_path,
                book_schema = book_schema,
                ratings_schema = ratings_schema,
                STATUS_FILE = STATUS_FILE_PATH
            )

            logging.info("Data Validation process Configuration creation successfull")
            return validation_configuration

        except Exception as e:
            logging.error(f"Error while creating Data Validation process Configuration: {e}", exc_info=True)
            raise AppException(e, sys)
        

    def data_transformation_config(self) -> DataTransformationConfig:
        """
        Creates the configuration for Data Transformation 
        Returns: DataTransformationConfig object
        """
        try:
            transformation_config = self.config.data_transformation
            validation_config = self.config.data_validation

            create_directories(transformation_config.root_dir)
            create_directories(transformation_config.serialized_obj_dir)
            create_directories(transformation_config.common_obj_dir)
            
            books_data = transformation_config.valid_books_dataset
            ratings_data = transformation_config.valid_ratings_dataset

            transformation_root_dir = Path(transformation_config.root_dir)
            serialized_obj_dir = Path(transformation_config.serialized_obj_dir)
            common_obj_dir = Path(transformation_config.common_obj_dir)
            books_data_path = Path(validation_config.root_dir, validation_config.valid_data_dir, books_data)
            ratings_data_path = Path(validation_config.root_dir, validation_config.valid_data_dir, ratings_data)

            transformation_configiguration = DataTransformationConfig(
                transformation_dir = transformation_root_dir,
                serialized_obj_dir = serialized_obj_dir,
                common_obj_dir = common_obj_dir,
                books_data_path = books_data_path,
                ratings_data_path = ratings_data_path,
            )

            logging.info("Data Transformation Configuration creation successfull")
            return transformation_configiguration

        except Exception as e:
            logging.error(f"Error while creating Data Transformation Configuration: {e}", exc_info=True)
            raise AppException(e, sys)
        

    def model_trainer_config(self) -> ModelTrainerConfig:
        """
        Creates the configuration for Model Training 
        Returns: ModelTrainerConfig object
        """
        try:
            trainer_config = self.config.model_trainer
            transformation_config = self.config.data_transformation

            create_directories(trainer_config.root_dir)

            trained_model_dir = Path(trainer_config.root_dir)
            trained_model = trainer_config.trained_model
            books_pivot_table = trainer_config.books_pivot_table

            books_pivot_table_path = Path(transformation_config.serialized_obj_dir, books_pivot_table)

            training_configuration = ModelTrainerConfig(
                trained_model_dir = trained_model_dir,
                books_pivot_table_path = books_pivot_table_path,
                model_name = trained_model
            )

            logging.info("Model Trainer Configuration creation successfull")
            return training_configuration

        except Exception as e:
            logging.error(f"Error while creating Model Trainer Configuration: {e}", exc_info=True)
            raise AppException(e, sys)
        

    def ml_recommendation_config(self) -> MLRecommendationConfig:
        """
        Creates the configuration for ML Recommender 
        Returns: MLRecommendationConfig object
        """
        try:
            recommender_config = self.config.ml_recommender
            serialized_obj_dir = recommender_config.serialized_obj_dir
            common_obj_dir = recommender_config.common_obj_dir
            
            book_names_obj_path = Path(common_obj_dir, "book_names.pkl")
            books_pivot_table_obj_path = Path(serialized_obj_dir, "books_pivot_table.pkl")
            final_ratings_obj_path = Path(serialized_obj_dir, "books_final_ratings.pkl")

            trained_model_path = Path(recommender_config.trained_model_dir, "model.pkl")
          
            ml_recommendation_configuration = MLRecommendationConfig(
                serialized_obj_dir = serialized_obj_dir,
                book_names_obj_path = book_names_obj_path,
                books_pivot_table_obj_path = books_pivot_table_obj_path,
                final_ratings_obj_path = final_ratings_obj_path,
                trained_model_path = trained_model_path
            )

            logging.info(f"ML-Recommender Configuration creation successfull")
            return ml_recommendation_configuration

        except Exception as e:
            logging.error(f"Error while creating ML-Recommender Configuration: {e}", exc_info=True)
            raise AppException(e, sys)
        

    def semantic_recommender_config(self) -> SemanticRecommendationConfig:
        """
        Creates the configuration for Semantic Recommender 
        Returns: SemanticRecommendationConfig object
        """
        try:
            recommender_config = self.config.semantic_recommender
        
            vectorstore_dir = Path(recommender_config.root_dir, recommender_config.vectorstore)
            books_obj_path = Path(recommender_config.root_dir, recommender_config.semantic_books_dataset)

            sm_recommendation_configuration =  SemanticRecommendationConfig(
                final_books_obj_path = books_obj_path,
                chroma_persist_dir = vectorstore_dir
            )

            logging.info(f"Semantic Recommender Configuration creation successfull")
            return sm_recommendation_configuration
        
        except Exception as e:
            logging.error(f"Error while creating Semantic Recommender Configuration: {e}", exc_info=True)
            raise AppException(e, sys)
        