FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry==1.8.3 && poetry install --no-dev
COPY app .
ENV PYTHONPATH=/app
RUN mkdir -p ./reports
RUN mkdir -p ./logs
RUN mkdir -p ./output_logs
WORKDIR /
CMD ["poetry","--directory", "/app", "run", "python", "-m", "log_analyzer.main"]
