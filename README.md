# pyspark-simple-learning

This project is a compact, clear PySpark example for practicing Spark locally (local mode). It focuses on reading data (text/CSV) → transforming/cleaning → summarizing (group/join/agg) using the DataFrame API and Spark SQL.

This README provides detailed installation steps, sanity checks, how to run the demo jobs, expected outputs, system design description, and instructions for the architecture diagram.

----

## Table of Contents

- Requirements
- Project structure
- Installation and getting started (step-by-step)
- Sanity checks and how to run the three demo scripts (with expected outputs)
- Verifying outputs (checklist)
- Clearing outputs and re-running
- System design and execution flow
- Diagram (SVG) and how to convert to PNG
- Troubleshooting (common issues and fixes)
- Next steps / exercises

----

## Requirements

1) Python

- Python 3.9+ (3.10/3.11 are supported)
- Use the `python` command if available; otherwise use `python3` (common on macOS)

2) Java (required for Spark)

- PySpark runs on the JVM and requires Java installed
- If you use Java 11, use PySpark 3.5.x (this project pins pyspark in requirements.txt as `pyspark>=3.5.0,<4.0`)
- If you want to use PySpark 4.x, install Java 17 and update requirements accordingly

Check Java version:

```bash
java -version
```

Example installation (macOS/Homebrew):

```bash
brew install openjdk@11
# or
brew install openjdk@17
```

Set JAVA_HOME (macOS example):

```bash
export JAVA_HOME=$(/usr/libexec/java_home -v 11)
# or
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

----

## Project structure

- src/
  - spark_session.py: helper to create a SparkSession configured for local runs
  - config.py: base paths and configuration (data/raw, data/output)
  - jobs/: example jobs runnable with `python -m src.jobs.<module>`
- data/raw/: sample input data
  - text.txt: sample text for wordcount
  - users.csv, orders.csv: sample data for ETL/SQL demos
- data/output/: output folder written by the jobs

Note: Spark `df.write.csv("path")` creates a folder `path/` containing `part-*.csv` files and a `_SUCCESS` marker file when the write completes successfully.

----

## Installation and getting started (step-by-step)

1. Open a terminal and change to the project root:

```bash
cd pyspark-simple-learning
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

(On Windows: `python -m venv .venv` then `\.venv\Scripts\Activate.ps1` or `\.venv\Scripts\activate`)

3. Upgrade pip and install dependencies:

```bash
pip install -U pip
pip install -r requirements.txt
```

4. Verify installation:

```bash
python -V
java -version
python -c "import pyspark; print('pyspark', pyspark.__version__)"
```

Expected:
- Java 11 or 17
- pyspark 3.5.x (as pinned)

----

## Sanity check (verify SparkSession)

Quick test to ensure SparkSession can be created:

```bash
python -c "from src.spark_session import get_spark; s=get_spark('smoke'); print(s.version); s.stop()"
```

If the command prints a Spark version without errors, the environment is ready to run the demo jobs.

----

## Running the three demo jobs (what they do and expected output)

Run from the project root with the virtual environment active.

1) WordCount (DataFrame API)

Run:

```bash
python -m src.jobs.wordcount
```

What it does:
- Reads `data/raw/text.txt`
- Lowercases text
- Splits words using regex `\W+`
- Explodes into one word per row
- groupBy to count occurrences
- Writes CSV output to `data/output/wordcount/`

Expected console output (example):
```
+----------+-----+
|word      |count|
+----------+-----+
|is        |4    |
|count     |3    |
|word      |3    |
|for       |2    |
|pyspark   |2    |
...       ...
+----------+-----+
```

Files produced:
- data/output/wordcount/part-*.csv
- data/output/wordcount/_SUCCESS

Inspect results (example using pandas):

```bash
python -c "import glob,pandas as pd; p=glob.glob('data/output/wordcount/part-*.csv')[0]; print(pd.read_csv(p).head(20))"
```

----

2) ETL: users + orders (join + aggregate)

Run:

```bash
python -m src.jobs.etl_users_orders
```

What it does:
- Reads `data/raw/users.csv` and `data/raw/orders.csv` (header + inferSchema)
- Cleans orders:
  - cast `amount` to double (non-numeric values become null)
  - parse `created_at` to timestamp
  - filter out rows where `amount` is null
- left join with `users` on `user_id`
- groupBy to compute `order_count`, `total_amount`, `last_order_at`
- Writes CSV to `data/output/users_orders_summary/`

Expected console output (example):
```
+-------+----+----------+-----------+------------+-------------------+
|user_id|name|city      |order_count|total_amount|last_order_at      |
+-------+----+----------+-----------+------------+-------------------+
|4      |Mai |Phuket    |1          |999.9       |2025-10-05 08:30:00|
|2      |Aom |Chiang Mai|1          |250.0       |2025-12-01 09:00:00|
|1      |Boyd|Bangkok   |2          |159.5       |2025-12-23 18:45:10|
|3      |Ken |Khon Kaen |2          |105.74      |2025-11-12 12:00:00|
|5      |Nok |Bangkok   |1          |60.0        |2025-12-31 23:59:59|
+-------+----+----------+-----------+------------+-------------------+
```

Inspect output:

```bash
python -c "import glob,pandas as pd; p=glob.glob('data/output/users_orders_summary/part-*.csv')[0]; print(pd.read_csv(p))"
```

----

3) Spark SQL demo (temp views + SQL)

Run:

```bash
python -m src.jobs.sql_demo
```

What it does:
- Reads `users.csv` and `orders.csv`
- Creates temporary views `users` and `orders`
- Runs a SQL query (JOIN + GROUP BY + ORDER BY) via `spark.sql(...)`

Expected console output (example):
```
+-------+----+----------+-----------+------------+
|user_id|name|city      |order_count|total_amount|
+-------+----+----------+-----------+------------+
|4      |Mai |Phuket    |1          |999.9       |
|2      |Aom |Chiang Mai|2          |250.0       |
|1      |Boyd|Bangkok   |2          |159.5       |
|3      |Ken |Khon Kaen |2          |105.74      |
|5      |Nok |Bangkok   |1          |60.0        |
+-------+----+----------+-----------+------------+
```

Note: The SQL demo uses `COUNT(DISTINCT o.order_id)` which may differ from the ETL demo in cases where `amount` is `N/A` because the ETL demo filters out rows with non-numeric amounts.

----

## Verifying outputs (checklist)

After running the demos, verify outputs exist:

```bash
python -c "import glob; assert glob.glob('data/output/wordcount/part-*.csv'), 'wordcount output missing'; assert glob.glob('data/output/users_orders_summary/part-*.csv'), 'users_orders_summary output missing'; print('OK: outputs exist')"
```

Clear outputs if you want to re-run from scratch:

```bash
rm -rf data/output/wordcount data/output/users_orders_summary
```

----

## System design & execution flow

High-level flow when a job in `src/jobs/` runs:

1. The Python job calls `get_spark()` from `src.spark_session` to create a configured SparkSession (entry point)
2. The SparkSession communicates with the JVM via Py4J and launches a SparkContext (local mode)
3. Spark reads data from `data/raw/` using the DataSource API into DataFrames
4. Transformations are applied (withColumn, cast, filter, split, explode, groupBy, join)
5. When `df.write...` is executed, Spark performs shuffles/aggregations as needed and writes outputs to `data/output/` as `part-*.csv`
6. The job stops the SparkSession (`s.stop()`) when finished

Important notes:
- Local runs use `master("local[*]")` and the repo reduces `spark.sql.shuffle.partitions` to a small number suitable for small local datasets
- `spark.driver.bindAddress` and `spark.driver.host` are set to `127.0.0.1` to avoid UnresolvedAddress issues on some machines
- Timezone handling: the project sets UTC to make timestamp conversions consistent

----

## Diagram (SVG located at `assets/architecture_diagram.svg`)

The diagram illustrates components and data flow for local execution.

If you want to convert the SVG to PNG locally (ImageMagick or rsvg-convert):

- ImageMagick:
```bash
convert assets/architecture_diagram.svg assets/architecture_diagram.png
```
- rsvg-convert:
```bash
rsvg-convert -f png -o assets/architecture_diagram.png assets/architecture_diagram.svg
```

----

## Troubleshooting (common issues)

1) ModuleNotFoundError: No module named 'pyspark'
- Cause: dependencies not installed or virtual environment not activated
- Fix:
  - source .venv/bin/activate
  - pip install -r requirements.txt

2) JAVA_GATEWAY_EXITED / UnsupportedClassVersionError
- Cause: Java version incompatible with the installed PySpark
- Fix:
  - Use Java 11 with PySpark 3.5.x
  - Or install Java 17 and update PySpark to 4.x if you need Spark 4

3) UnresolvedAddressException when starting Spark
- Cause: hostname or bind address issues
- Fix:
  - Check `src/spark_session.py` and ensure `spark.driver.bindAddress` and `spark.driver.host` are set to `127.0.0.1`

----

## Next steps / exercises

- Add new columns with `withColumn` (e.g., bucket total_amount)
- Filter for specific cities (e.g., `city='Bangkok'`)
- Add `avg(amount)`, `min`, `max` to aggregations
- Compare inner vs left joins and observe row counts
- Change output format to Parquet and read back with `spark.read.parquet`
- Refactor job logic into smaller functions and add assertions for row counts or totals

----