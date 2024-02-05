FROM python:3.11
COPY ./app /app/app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
WORKDIR /app/app
ENV PYTHONPATH=/app/app
CMD uvicorn main:app --reload --host 0.0.0.0 --port 80