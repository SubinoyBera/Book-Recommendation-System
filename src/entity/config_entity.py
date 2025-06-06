from collections import namedtuple

DataIngestionConfig = namedtuple("DatasetConfig", ["data_download_url",
                                                   "raw_data_dir",
                                                   "ingested_dir"])