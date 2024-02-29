from python:3.11
COPY ./SidMixtralTogetherAIBackend /app
COPY ./Sid67 /packages/Sid67
ENV PYTHONPATH=/packages;/app
WORKDIR /app
RUN pip install -r requirements.txt