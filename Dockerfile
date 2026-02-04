FROM python:3.11-slim

WORKDIR /commodity-tracker

COPY assets/requirements.txt .
COPY scripts/ scripts/
COPY data/ data/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "scripts/get-price.py"]

