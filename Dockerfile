# Use slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip and install only CPU-friendly packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir torch==2.0.1+cpu torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port for FastAPI
EXPOSE 10000

# Start FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
