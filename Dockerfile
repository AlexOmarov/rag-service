FROM nvidia/cuda:12.5.1-cudnn-devel-ubuntu22.04

RUN apt-get update && apt-get --no-install-recommends -y install build-essential gcc libsndfile1 wget && apt-get clean

WORKDIR /app

COPY ./src ./src
COPY pyproject.toml ./pyproject.toml

RUN apt-get update && \
    apt-get --no-install-recommends -y install build-essential gcc libsndfile1 wget && apt-get clean && \
    wget -qO- https://github.com/astral-sh/uv/releases/download/0.7.9/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz -C /usr/local/bin && \
    chmod +x /usr/local/bin/uv-x86_64-unknown-linux-gnu/uv

ENV PATH="/app/.venv/bin:$PATH"
ENV PATH="/usr/local/bin/uv-x86_64-unknown-linux-gnu:$PATH"

RUN uv sync --no-install-project --no-dev && \
    chmod +x /app/.venv/bin/python3

# Expose the port
EXPOSE 5000

# Entry point runs python inside uv environment
ENTRYPOINT ["uv", "run", "uvicorn", "src.main.app.app:app", "--host", "0.0.0.0", "--port", "5000"]
