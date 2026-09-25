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

---

## Day 3 - Pandas Cleaning and Data Quality

**Files:** day3/day3_cleaning.py, day3/cleaning_utils.py, day3/config.json

### How to run
    python day3\day3_cleaning.py

### What it does
- Profiles all four datasets (customers, products, orders, order_items) -
  rows, columns, dtypes, null counts, and duplicate key counts (Lab 3.1)
- Cleans customers: trims/title-cases names, lowercases email,
  standardizes city/state, parses signup_date (Lab 3.2)
- Cleans products: converts prices to numeric, rejects missing IDs and
  any row where cost_price is greater than list_price (Lab 3.3)
- Cleans orders: parses order_date, validates order_status and
  sales_channel against the accepted value lists, rejects orders
  referencing an unknown customer_id (Lab 3.4)
- Cleans order_items: validates quantity (>0), unit_price (>=0),
  discount_pct (0-100), and rejects rows with an unknown order_id or
  product_id foreign key (Lab 3.5)
- Combines all four datasets' rejected rows into one file, tagged with
  which dataset they came from and a timestamp for the run (Lab 3.6)
- Builds a per-dataset quality report: input, valid, rejected,
  duplicate, and missing-key counts (Lab 3.7)

### Duplicate handling
Every dataset's primary key is checked with pandas' duplicated(keep="first"):
The first row with a given ID is treated as valid, and every later row
sharing that same ID is rejected with reason "duplicate <field>". This
keeps each key unique in the cleaned output while preserving a record of
every duplicate in all_rejects.csv, rather than silently dropping them.

### Outputs
- data/output/clean_customers.csv, clean_products.csv, clean_orders.csv,
  clean_order_items.csv
- data/output/data_quality_report.csv
- data/rejects/all_rejects.csv

### Config
Folder paths are read from config.json (data_input, data_output,
data_rejects, log) rather than hardcoded, same as Day 2.

---

## Day 4 - Pandas Transformations and Reconciliation

**Files:** day4/day4_transform.py, day4/config.json

### How to run
    python day4\day4_transform.py

Reads only the clean files produced by Day 3 (day3/data/output/) -
no raw data is transformed directly, per the project's business rules.

### What it does
- Merges clean_order_items, clean_orders, clean_customers and
  clean_products into one row per order item, excluding Cancelled
  orders from the sales fact (Lab 4.1)
- Calculates gross sales, discount, net sales, total cost, gross
  profit and profit margin as columns on fact_sales.csv (Lab 4.2)
- Builds summary tables by customer, product, category, state,
  sales channel and month (Lab 4.3)
- Ranks the top 10 customers and top 10 products by net sales, and
  the top 3 products within each category (Lab 4.4)
- Calculates previous-month sales and month-over-month growth per
  month in monthly_sales.csv (Lab 4.5)
- Builds a category-by-month revenue pivot table (Lab 4.6)
- Reconciles the fact table against the source data: confirms
  order_item_id is unique, the fact row count matches the expected
  count (source order items minus Cancelled orders), and detail
  revenue equals summary revenue (Lab 4.7)

### Outputs
- data/output/fact_sales.csv
- data/output/customer_summary.csv, product_summary.csv,
  category_summary.csv, state_summary.csv, channel_summary.csv,
  monthly_summary.csv
- data/output/top_10_customers.csv, top_10_products.csv,
  top_3_products_category.csv
- data/output/monthly_sales.csv
- data/output/category_month_pivot.csv
- data/output/reconciliation_report.csv

### Config
Points data_input directly at day3/data/output rather than keeping a
separate copy of the clean files - Day 4 has no rejects and no
logging requirement, so config.json only needs data_input and
data_output.
