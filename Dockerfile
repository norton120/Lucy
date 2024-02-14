FROM python:3.11
COPY ./fastapi_test /app
COPY ./MemGPT /packages/MemGPT
COPY ./src /packages/sid
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install poetry
WORKDIR /packages/MemGPT
RUN poetry install --no-root
WORKDIR /app/app
ENV PYTHONPATH=/app/app:/packages/MemGPT:/packages/sid
CMD uvicorn main:app --reload --host 0.0.0.0 --port 80