# File: main.py
import sys
from src.core.logger import logging
from src.core.exception import AppException
from src.pipeline.ml_pipeline import MLPipeline

# Main entry point for the ML pipeline execution
# This script initializes the ML pipeline and starts the main process.
try:
    logging.info("Initializing ML Pipeline")
    pipeline = MLPipeline()
    pipeline.main()
    logging.info("Pipeline executed successfully")
        
except Exception as e:
    logging.error(f"ML pipeline terminated: {e}", exc_info=True)
    raise AppException(e, sys)