import argparse
import pandas as pd
import numpy as np
import yaml
import logging

import json
import time
import sys
import os


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path):
    if not os.path.exists(config_path):
        raise ValueError("config file not found")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    for key in ["seed", "window", "version"]:
        if key not in config:
            raise ValueError(f"missing config key: {key}")

    return config


def load_data(input_path):
    if not os.path.exists(input_path):
        raise ValueError("input csv not found")

    df = pd.read_csv(input_path)

    if df.empty:
        raise ValueError("csv is empty")

    if len(df.columns) == 1:
        temp = df.iloc[:, 0].str.split(",", expand=True)
        temp.columns = ["timestamp", "open", "high", "low", "close", "volume_btc", "volume_usd"]
        df = temp

    df.columns = df.columns.str.strip().str.lower()

    if "close" not in df.columns:
        raise ValueError(f"missing close column: {list(df.columns)}")

    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logger(args.log_file)
    start_time = time.time()

    try:
        config = load_config(args.config)
        np.random.seed(config["seed"])

        df = load_data(args.input)

        df["rolling_mean"] = df["close"].rolling(window=config["window"]).mean()
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        df = df.dropna()

        metrics = {
            "version": config["version"],
            "rows_processed": len(df),
            "metric": "signal_rate",
            "value": round(float(df["signal"].mean()), 4),
            "latency_ms": int((time.time() - start_time) * 1000),
            "seed": config["seed"],
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(metrics, f, indent=4)

        print(json.dumps(metrics, indent=4))

    except Exception as e:
        error = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error, f, indent=4)

        print(json.dumps(error, indent=4))


if __name__ == "__main__":
    main()