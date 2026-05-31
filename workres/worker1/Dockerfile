FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY workres/worker1/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY workres/worker1/worker.py ./worker.py

CMD ["python", "worker.py"]
