FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

ENV PYTHONUNBUFFERED=1
# En PROD usás gunicorn (tu compose ya lo pasa por command)
# En DEV el compose corre "flask run"
