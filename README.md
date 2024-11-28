# Log Analyzer

`Log Analyzer` is a Python-based tool designed to analyze `nginx` logs and generate HTML reports highlighting the most "
problematic" URLs based on request processing times (`$request_time`).

## Features

- **Log Analysis:**
    - Processes logs (both gzip and plain formats) from a specified directory.
    - Identifies the most time-consuming URLs and calculates key statistics.

- **HTML Report Generation:**
    - Creates a sortable report in HTML format, including metrics like:
        - `count`: Total number of requests.
        - `count_perc`: Percentage of total requests.
        - `time_sum`: Total request processing time.
        - `time_perc`: Percentage of total request time.
        - `time_avg`: Average request processing time.
        - `time_max`: Maximum request processing time.
        - `time_med`: Median request processing time.

- **Error Handling:**
    - Logs unparsable lines and exits if the error threshold (configured) is exceeded.
    - Automatically skips logs if a report for the same date already exists.

- **Custom Configuration:**
    - Supports configurable log directories, report sizes, and error thresholds via a JSON configuration file.

## Installation

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) for dependency management

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/trifonovtema/log-analyzer.git
   poetry install
   poetry run pre-commit install
    ```

# Configuration
## Create a JSON configuration file (e.g., config.json) with the following structure:

```json
{
    "LOG_DIR": "./logs",
    "REPORT_DIR": "./reports",
    "REPORT_SIZE": 1000,
    "ERROR_THRESHOLD": 0.1,
    "LOG_FILE": "./log_analyzer.log"
}
```
## Configuration Fields
```
| Field            | Default Value  | Description
|------------------|----------------|-------------------------------------------------------------------------
| `LOG_DIR`        | `./logs`       | Directory containing the logs to analyze.
| `REPORT_DIR`     | `./reports`    | Directory to store generated HTML reports.
| `REPORT_SIZE`    | `1000`         | Number of top URLs to include in the report.
| `ERROR_THRESHOLD`| `0.1`          | Maximum allowable ratio of unparsable lines before stopping execution.
| `LOG_FILE`       | `None`         | File to log application messages (if not set, logs are printed to stdout).
```

# Usage
## Running the Analyzer
To analyze logs and generate a report:
```bash
poetry run python -m log_analyzer.main --config ./sample_config.json
```
## Options
`--config`: Path to the configuration file (default: ./config.json).

# Running Tests
## Run unit tests using pytest:

```bash
make test
```

# Code Formatting and Linting
Ensure code quality using the following commands:

Format code with black:

```bash
make format
```
Check imports with isort:

```bash
make lint
```

# Report Format
The HTML report includes a table summarizing URL statistics

# Docker Support
To run the analyzer in a Docker container:

Build the Docker image:

```bash
docker build -t log-analyzer .
```

Run the container:

```bash
docker run --rm -v $(pwd)/logs:/app/logs -v $(pwd)/reports:/app/reports log-analyzer
```

# Development
## Development Commands
Run tests:

```bash
make test
```

Format code:

```bash
make format
```

Run the application:

```bash
make run
```
