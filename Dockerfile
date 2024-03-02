FROM python:3.11
COPY ./fastapi_test /app
COPY ./Lucy /packages/Lucy
WORKDIR /app/app
RUN pip install --no-cache-dir -r /app/requirements.txt
ENV PYTHONPATH=/app/app:/packages/Lucy
CMD uvicorn main:app --reload --host 0.0.0.0 --port 80