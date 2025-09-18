# Use official Python image
FROM python:3.12

# Metadata
LABEL authors="aishwaryabharambe"

# Set working directory
WORKDIR /code

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./BookLibraryApp /code/BookLibraryApp

# Expose port 80
EXPOSE 8000

# Run FastAPI using Uvicorn
CMD ["uvicorn", "BookLibraryApp.main:app", "--host", "0.0.0.0", "--port", "8000"]