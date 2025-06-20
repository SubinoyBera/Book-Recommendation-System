## This module defines configuration entities
## Each configuration is represented as a dataclass, which provides a clear structure for the parameters needed in each step of the machine learning pipeline.

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    data_download_url: str
    raw_data_dir: Path
    ingested_dir: Path

@dataclass(frozen=True)
class DataValidationConfig:
    valid_data_dir: Path
    books_csvfile: Path
    ratings_csvfile: Path
    book_schema: dict
    ratings_schema: dict
    STATUS_FILE: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    transformation_dir: Path
    serialized_obj_dir: Path
    common_obj_dir: Path
    books_data_path: Path
    ratings_data_path: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    trained_model_dir: Path
    books_pivot_table_path : Path
    model_name: str

@dataclass(frozen=True)
class MLRecommendationConfig:
    serialized_obj_dir: Path
    book_names_obj_path: Path
    books_pivot_table_obj_path: Path
    final_ratings_obj_path: Path
    trained_model_path: Path

@dataclass(frozen=True)
class SemanticRecommendationConfig:
    final_books_obj_path: Path
    chroma_persist_dir: Path