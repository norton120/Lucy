from python:3.11
COPY ./SidMixtralTogetherAIBackend /app
COPY ./Sid67/sid67 /packages/sid67
ENV PYTHONPATH=/packages:/app
WORKDIR /app
RUN pip install -r requirements.txt