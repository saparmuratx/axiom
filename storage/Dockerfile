FROM ghcr.io/astral-sh/uv:trixie-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev libev-dev python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

RUN uv pip install cassandra-driver==3.29.3

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
