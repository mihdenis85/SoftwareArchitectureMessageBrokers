FROM python:3.12-slim

WORKDIR /app

COPY user_facing/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY user_facing/main.py ./
COPY common/ ./common/

CMD ["python", "main.py"]
