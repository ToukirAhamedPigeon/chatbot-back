FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

# CPU-only PyTorch stack
RUN pip install torch==2.1.1+cpu torchvision==0.16.1+cpu torchaudio==2.1.0 -f https://download.pytorch.org/whl/cpu/torch_stable.html

# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
