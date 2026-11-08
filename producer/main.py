#!/usr/bin/env python3
"""Publish demo electronics orders to Kafka."""

import argparse
import json
import random
import time
from datetime import datetime, timezone
from uuid import uuid4

from kafka import KafkaProducer


PRODUCTS = (
    ("Smartphone X", "smartphones", 799.99),
    ("UltraBook 14", "laptops", 1299.00),
    ("Noise-Cancelling Headphones", "audio", 249.50),
    ("4K Monitor", "monitors", 459.90),
    ("Mechanical Keyboard", "accessories", 119.00),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap-servers", default="kafka:9092")
    parser.add_argument("--topic", default="electronics-orders")
    parser.add_argument("--messages", type=int, default=10)
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def build_order(randomizer: random.Random) -> dict:
    product, category, price = randomizer.choice(PRODUCTS)
    return {
        "order_id": str(uuid4()),
        "customer": f"customer-{randomizer.randint(1000, 9999)}",
        "product": product,
        "category": category,
        "price": price,
        "quantity": randomizer.randint(1, 3),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    args = parse_args()
    if args.messages < 1:
        raise ValueError("--messages must be greater than zero")
    if args.interval < 0:
        raise ValueError("--interval cannot be negative")

    randomizer = random.Random(args.seed)
    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda value: value.encode("utf-8"),
    )
    try:
        for _ in range(args.messages):
            order = build_order(randomizer)
            producer.send(args.topic, key=order["order_id"], value=order).get(
                timeout=30
            )
            print(json.dumps(order), flush=True)
            time.sleep(args.interval)
        producer.flush()
    finally:
        producer.close()


if __name__ == "__main__":
    main()
