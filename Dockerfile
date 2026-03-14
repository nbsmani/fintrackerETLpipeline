#Base image
FROM python:3.11-slim

#Set the working directory in the container
WORKDIR /commodity-tracker

# Copy the requirements file and install dependencies
COPY assets/requirements.txt .
COPY scripts/ scripts/
COPY data/ data/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Make scripts executable
RUN chmod +x scripts/extract/*.py
RUN chmod +x scripts/load/*.py

# Set the entry point to run the get-price.py script
ENTRYPOINT ["python"]