# MLOps Batch Pipeline Task

## Overview

This project implements a minimal MLOps-style batch pipeline with:

* Config-driven execution using YAML
* Deterministic results via seed
* Data validation and error handling
* Structured logging
* Machine-readable metrics output
* Dockerized execution

---

## Local Run Instructions

### 1. Install dependencies

pip install -r requirements.txt

### 2. Run the pipeline

python run.py --input data.csv --config config.yaml --output metrics.json --log-file run.log

---

## Docker Instructions

### Build Docker image

docker build -t mlops-task .

### Run container

docker run --rm mlops-task

---

## Example metrics.json

{
"version": "v1",
"rows_processed": 9996,
"metric": "signal_rate",
"value": 0.4991,
"latency_ms": 217,
"seed": 42,
"status": "success"
}

---

## Notes

* Uses only the `close` column for signal generation
* Handles malformed CSV input gracefully
* Ensures reproducibility using fixed seed
* Writes metrics in both success and error cases
