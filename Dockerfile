# Dockerfile for the application

# Python base image
FROM python:3.11.13-alpine3.21

# Upgrade and Install build dependencies 
RUN apt-get update && apt-get upgrade -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose streamlit port
EXPOSE 8501

# Entry point to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]