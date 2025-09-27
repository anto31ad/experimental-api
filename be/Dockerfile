FROM python:3.11-slim

WORKDIR /app

# Ensure you are copying the requirements file
COPY requirements.txt .

# Install dependencies before copying the rest of your code
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
