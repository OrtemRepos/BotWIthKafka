FROM ghcr.io/astral-sh/uv:0.4.17-python3.12-bookworm

ENV UV_PYTHON_PREFERENCE=only-system

ARG PYTHONPATH
ENV PYTHONPATH=$PYTHONPATH:/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get install curl -y

WORKDIR /app

ADD ./requirements.txt ./

RUN uv pip install --system -r requirements.txt

ADD ./src /app/src

CMD ["uv", "run", "src/main.py"]

EXPOSE 8002