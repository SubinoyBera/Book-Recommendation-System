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