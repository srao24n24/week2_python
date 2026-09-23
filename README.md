# Week 2 — Python Data Engineering Candidate Labs

Progressive 6-day project building a retail sales mini ETL pipeline in
Python. Each day builds on the previous day's output — Day 1 covers core
Python fundamentals, Day 2 adds file I/O, validation, exceptions and
logging, and later days bring in Pandas, SQL Server loading, and a final
independent assessment.

Project root: `Week2_Python/`. All scripts are run from this root
directory (not from inside their own day folder), e.g.:

    python day1\day1_order_analyzer.py
    python day2\day2_ingestion.py

---

## Day 1 — Python Foundations

**Files:** `day1/day1_order_analyzer.py`, `day1/sales_utils.py`

### How to run
    python day1\day1_order_analyzer.py

### What it does
- Calculates line totals, gross value, discount, net value and total
  quantity from a fixed set of order tuples
- Classifies orders (Small/Medium/Large) and determines delivery status
  using conditional logic
- Tracks unique products (set) and per-product quantities (dict)
- Reusable calculation functions live in `sales_utils.py` and are
  imported into the main script
- Includes two required comprehension outputs (set/dict comprehensions)

### Output
Console output only — printed order summary, verified against the
control totals in `day1_input_and_check.txt` (total quantity: 8, gross:
140400.00, discount: 14040.00, net: 126360.00).

---

## Day 2 — Files, Exceptions and Logging

**Files:** `day2/day2_ingestion.py`, `day2/validation_utils.py`,
`day2/config.json`

### How to run
    python day2\day2_ingestion.py

### What it does
- Discovers CSV/JSON files in the input folder (Lab 2.1)
- Loads customers.csv and products.json (Lab 2.2)
- Validates file structure — exists, non-empty, required fields (Lab 2.3)
- Validates individual records — IDs, dates, prices — splitting into
  valid and rejected records with a reason per reject (Lab 2.4)
- Raises `DataValidationError` for file-level failures (Lab 2.5)
- Logs the full run to console and `log/pipeline.log` (Lab 2.6)

### Outputs
- `data/output/customers_valid.csv`, `data/output/products_valid.json`
- `data/rejects/customers_rejects.csv`, `data/rejects/products_rejects.json`
- `log/pipeline.log`

### Config
Folder paths are read from `config.json` (`data_input`, `data_output`,
`data_rejects`, `log`) rather than hardcoded.
