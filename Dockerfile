FROM python:3.11-slim AS builder
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock ./
COPY tg_mailcow_aliases ./tg_mailcow_aliases
RUN poetry build --format wheel

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app/dist/*.whl .
RUN pip install *.whl && rm *.whl
CMD ["start"]
