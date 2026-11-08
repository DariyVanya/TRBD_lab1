#!/usr/bin/env python3
"""Consume electronics orders and persist them as JSON batches."""

import argparse
import json
from pathlib import Path
from typing import Any

from kafka import KafkaConsumer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap-servers", default="kafka:9092")
    parser.add_argument("--topic", default="electronics-orders")
    parser.add_argument("--output", default="/data/orders.json")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args()


def write_batch(output: Path, batch: list[dict[str, Any]]) -> None:
    existing: list[dict[str, Any]] = []
    if output.exists():
        existing = json.loads(output.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(existing + batch, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    if args.batch_size < 1:
        raise ValueError("--batch-size must be greater than zero")
    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than zero")

    output = Path(args.output)
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="electronics-json-writer",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        consumer_timeout_ms=int(args.timeout * 1000),
    )
    incoming: list[dict[str, Any]] = []
    try:
        batch: list[dict[str, Any]] = []
        for message in consumer:
            batch.append(message.value)
            incoming.append(message.value)
            if len(batch) >= args.batch_size:
                write_batch(output, batch)
                print(f"Wrote batch of {len(batch)} records to {output}", flush=True)
                batch = []
        if batch:
            write_batch(output, batch)
            print(f"Wrote batch of {len(batch)} records to {output}", flush=True)
    finally:
        consumer.close()

    persisted = json.loads(output.read_text(encoding="utf-8")) if output.exists() else []
    if incoming and persisted[-len(incoming) :] != incoming:
        raise RuntimeError("Persisted JSON does not match the incoming Kafka records")
    print(
        f"Verified {len(incoming)} incoming records against {output}",
        flush=True,
    )


if __name__ == "__main__":
    main()
