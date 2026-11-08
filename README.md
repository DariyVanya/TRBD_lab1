# Kafka electronics store lab

The lab demonstrates a producer and consumer for an electronics store. The
producer sends order JSON documents to Kafka; the consumer writes them to
`data/orders.json` in batches and verifies that the persisted records match
the records it received.

## CLI arguments

### Producer

```text
--bootstrap-servers  Kafka connection (default: kafka:9092)
--topic              Topic name (default: electronics-orders)
--messages           Number of orders (default: 10)
--interval           Delay between orders in seconds (default: 1.0)
--seed               Optional random seed
```

### Consumer

```text
--bootstrap-servers  Kafka connection (default: kafka:9092)
--topic              Topic name (default: electronics-orders)
--output             JSON output path (default: /data/orders.json)
--batch-size         Records written per batch (default: 5)
--timeout             Stop after this many seconds without a record (default: 30)
```

## Run with Docker Compose

From `lab1/`:

```shell
docker compose up --build
```

The output is written to `lab1/data/orders.json`. The consumer exits after
the configured Kafka idle timeout and prints a verification message.

To inspect CLI help:

```shell
docker compose run --rm producer python producer/main.py --help
docker compose run --rm consumer python consumer/main.py --help
```

## Smoke tests

The lab has lightweight tests without an additional test framework. They
check Python syntax, both CLI help screens, the producer order structure, and
the JSON equality verification.

On Windows, run all tests with one command:

```powershell
.\scripts\run_tests.cmd
```

If PowerShell script execution is enabled, this is also available:

```powershell
.\scripts\run_tests.ps1
```

The equivalent command on any platform is:

```shell
python -m unittest discover -s tests -p "test_*.py" -v
```

To run the full Kafka integration demo and verify the consumer output:

```powershell
docker compose down --remove-orphans
docker compose up --build
```

The run is successful when the consumer logs contain:

```text
Verified 10 incoming records against /data/orders.json
```

The resulting file is available at `data/orders.json`.
