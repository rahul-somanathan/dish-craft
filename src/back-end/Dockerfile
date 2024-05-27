FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./src/back-end /app
COPY ./models/knn-model /app/models/knn-model
COPY ./data/processed/knn-model/train.pkl /app/data/processed/knn-model/train.pkl
COPY ./data/processed/knn-model/test.pkl /app/data/processed/knn-model/test.pkl
COPY ./data/processed/knn-model/train_sparse_matrix.pkl /app/data/processed/knn-model/train_sparse_matrix.pkl
COPY ./data/processed/knn-model/user_mapping.pkl /app/data/processed/knn-model/user_mapping.pkl
COPY ./data/processed/knn-model/recipe_mapping.pkl /app/data/processed/knn-model/recipe_mapping.pkl

# Install gcc and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]