from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["data_download_url",
                                                   "raw_data_dir",
                                                   "ingested_dir"])


DataValidationConfig = namedtuple("DataValidation", ["clean_data_dir",
                                                    "books_csvfile",
                                                     "ratings_csvfile",
                                                     "serialized_objects_dir"])
