# Use Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Copy requirements.txt first
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install CPU-only torch first from official PyTorch CPU index
RUN pip install torch==2.1.0+cpu torchvision==0.16.1+cpu torchaudio==2.1.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Then install the rest
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
