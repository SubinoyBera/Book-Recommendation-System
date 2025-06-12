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
    books_data_path: Path
    ratings_data_path: Path


@dataclass(frozen=True)
class ModelTrainerConfig:
    trained_model_dir: Path
    model_name: str
