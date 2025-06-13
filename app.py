import os
import sys
import pickle
import numpy as np
import streamlit as st
from src.logger import logging
from src.exception import AppException
from src.pipeline import ml_pipeline

if __name__ == "__main__":
    st.header("Book Recommender System")