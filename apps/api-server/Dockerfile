FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /workspace

COPY apps/api-server/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /workspace

WORKDIR /workspace/apps/api-server

EXPOSE 2048

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2048"]
