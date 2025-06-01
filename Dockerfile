FROM nvidia/cuda:12.5.1-cudnn-devel-ubuntu20.04

RUN apt-get update && apt-get --no-install-recommends -y install build-essential gcc libsndfile1 wget && apt-get clean

WORKDIR /app

COPY ./src ./src
COPY pyproject.toml ./pyproject.toml

RUN wget -qO- https://github.com/patrickjahns/uv/releases/latest/download/uv-linux-amd64.tar.gz | tar -xz -C /usr/local/bin && \
    uv sync --without groups && \
    useradd -ms /bin/bash app

USER app

SHELL ["uv", "shell", "--", "/bin/bash", "-c"]

# Expose the port
EXPOSE 5000

# Entry point runs python inside uv environment
ENTRYPOINT ["uv", "run", "python", "src/main/app/app.py"]