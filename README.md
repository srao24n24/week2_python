


# Day 2 — Files, Exceptions and Logging

## How to run
From the project root (`Week2_Python/`):

    python day2\day2_ingestion.py

## What it does
- Discovers CSV/JSON files in the input folder (Lab 2.1)
- Loads customers.csv and products.json (Lab 2.2)
- Validates file structure — exists, non-empty, required fields (Lab 2.3)
- Validates individual records — IDs, dates, prices — splitting into
  valid and rejected records with a reason per reject (Lab 2.4)
- Raises DataValidationError for file-level failures (Lab 2.5)
- Logs the full run to console and log/pipeline.log (Lab 2.6)

## Outputs
- data/output/customers_valid.csv, data/output/products_valid.json
- data/rejects/customers_rejects.csv, data/rejects/products_rejects.json
- log/pipeline.log

## Config
Folder paths are read from config.json (data_input, data_output,
data_rejects, log) rather than hardcoded.