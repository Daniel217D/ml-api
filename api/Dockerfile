FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api ./api

RUN chmod +x ./api/scripts/docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["sh", "./api/scripts/docker-entrypoint.sh"]
