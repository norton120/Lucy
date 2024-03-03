from python:3.11 as base
ARG ENVIRONMENT=production
COPY ./Lucy/lucy /app/lucy
COPY ./Lucy/requirements /app/requirements
ENV PYTHONPATH=/app:/packages
WORKDIR /app
RUN pip install -r /app/requirements/$ENVIRONMENT.requirements.txt


FROM base as development
ARG ENVIRONMENT=development
RUN pip install -r /app/requirements/$ENVIRONMENT.requirements.txt

FROM development as testing
COPY ./Lucy/dependency_stubs/stub_llm_backend /packages/stub_llm_backend