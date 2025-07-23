FROM python:3.10-slim

WORKDIR /app

RUN pip install --upgrade pip
    
# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code
COPY src/ .

ENTRYPOINT ["python", "entrypoint.py"]
