FROM python:3.12-slim

WORKDIR /app

COPY publish_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common/ ./common/
COPY publish_service/main.py ./

CMD ["python", "main.py"]
