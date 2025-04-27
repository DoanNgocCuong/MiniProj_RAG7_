#!/bin/bash

echo "Setting up Python virtual environment for FlashRAG..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Install Faiss
conda install -c pytorch faiss-cpu=1.8.0

echo "Setup completed successfully!"
echo "To activate the environment, run: source venv/bin/activate" 