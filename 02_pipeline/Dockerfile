# GPTQ-for-LLaMa and Text Generation WebUI Dockerfile
FROM nvidia/cuda:11.7.0-devel-ubuntu22.04 as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install --no-install-recommends -y build-essential python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*

COPY input.txt requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip pip3 install -r requirements.txt

COPY . .

#CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
CMD ["python3", "server.py" ]
