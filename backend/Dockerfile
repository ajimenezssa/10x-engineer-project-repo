# Step 1: Use Python base image
FROM python:3.11-slim

# Step 2: Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set working directory
WORKDIR /app

# Step 4: Install system tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Copy your app code
COPY ./app ./app

# Step 7: Expose port 8000 (FastAPI default)
EXPOSE 8000

# Step 8: Default command to run the app
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]