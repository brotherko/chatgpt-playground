# FROM tiangolo/uvicorn-gunicorn:python3.10-slim
# WORKDIR /app
# RUN pip install poetry
# COPY pyproject.toml poetry.lock ./
# RUN poetry export --without-hashes -f requirements.txt > requirements.txt
# RUN pip install -r requirements.txt
# COPY gptpg_server ./gptpg_server
# ENTRYPOINT ["python", "-m", "gptpg_server.main"]

FROM python:3.11 as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn:python3.11-slim
WORKDIR /app
COPY --from=requirements-stage /tmp/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY gptpg_server ./gptpg_server
CMD ["uvicorn", "gptpg_server.main:asgi_app", "--host", "0.0.0.0", "--port", "80"]

