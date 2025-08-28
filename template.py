# This script creates the required file structure for a project.
# It creates directories and files as specified in the list of file paths.
import os
from pathlib import Path

# List of files and directories to be created
files_list = [
    ".github/.gitkeep",
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/data_validation.py",
    "src/components/data_transformation.py",
    "src/components/model_trainer.py",
    "src/components/model_evaluation.py",
    "src/pipeline/__init__.py",
    "src/pipeline/ml_pipeline.py",
    "src/core/__init__.py",
    "src/core/config_entity.py",
    "src/constants/__init__.py",
    "src/core/exception.py",
    "src/core/logger.py",
    "src/core/exception.py",
    "src/utils/__init__.py",
    "notebooks/test.ipynb",
    "Dockerfile",
    ".dockerignore",
    "main.py",
    "app.py",
    "setup.py",
    "requirements.txt"
    "requirements-dev.txt"
]

# Create directories and files
for filepath in files_list:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath, 'w') as f:
            pass    # creates an empty file
    else:
        print(f"File already exists at {filepath}")