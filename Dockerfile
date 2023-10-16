FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1

# First copy only requirements.txt to cache dependencies independently
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 80
EXPOSE 4000

ENV UVICORN_HOST=0.0.0.0 UVICORN_PORT=[80,4000] UVICORN_LOG_LEVEL=info

CMD ["/bin/bash", "-c", "chmod +x /app/pre-start.sh && /app/pre-start.sh && uvicorn app.main:app --host 0.0.0.0 --port 80 "]
