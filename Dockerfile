FROM python:3.12-slim
WORKDIR /log_analyzer
COPY pyproject.toml poetry.lock ./
RUN pip install poetry==1.8.3 && poetry install --no-dev
COPY ./log_analyzer .
ENV PYTHONPATH=/log_analyzer
RUN mkdir -p ./reports
RUN mkdir -p ./logs
RUN mkdir -p ./output_logs
WORKDIR /
CMD ["poetry","--directory", "/log_analyzer", "run", "python", "-m", "log_analyzer.main"]
