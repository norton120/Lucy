FROM python:3.11
COPY . /app
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app
RUN uvicorn app:app --reload --host 0.0.0.0