FROM python:3.12-slim

WORKDIR /app

COPY filter_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY filter_service/main.py ./
COPY common/ ./common/

CMD ["python", "main.py"]
