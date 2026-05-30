# example-distributed-tracing
example repository for distributed tracing implementation

## Setup
- Install 'uv'
- Setup the environment using `uv venv`
- Install libraries from the `lock` file or `pyproject.toml` using `uv sync`

## Simple Auto Instrumentation Example
- Open the first terminal and run this command
    ```
    OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION=true opentelemetry-instrument \
        --traces_exporter console \
        --metrics_exporter console \
        --logs_exporter console \
        uvicorn app:app --host 0.0.0.0 --port 8000
    ```
- Send a request from the second terminal `curl http://0.0.0.0:8000/run`
- In the first terminal, logs will come along with a large `JSON` containing trace information
