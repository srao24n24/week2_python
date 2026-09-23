# -------- Data Ingestion --------
import json
import csv
import logging
from pathlib import Path
from validation_utils import(
    DataValidationError,
    validate_file_structure,
    validate_records
)

with open("day2/config.json") as f:
    config = json.load(f)

# --- Logging setup ---
log_folder = Path(config["log"])
log_folder.mkdir(parents = True, exist_ok = True)

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s",
    handlers = [logging.FileHandler(log_folder / "pipeline.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

logger.info("Pipeline started")

# --- Lab 2.1 ---
input_folder = Path(config["data_input"])
discovered_files = []

for files in input_folder.iterdir():
    if files.suffix in [".csv", ".json"]:
        discovered_files.append(files)

logger.info(f"Discovered {len(discovered_files)} files: {[f.name for f in discovered_files]}")

# --- Lab 2.2 ---
with open(input_folder/"customers.csv") as cus_f:
    reader = csv.DictReader(cus_f)
    customers = list(reader)

with open(input_folder/"products.json") as prod_f:
    products = json.load(prod_f)

logger.info(f"Customers loaded: {len(customers)}")
logger.info(f"Products loaded: {len(products)}")

# --- Lab 2.3 ---
cus_fields = ["customer_id", "customer_name", "email", "city", "state", "signup_date", "customer_segment"]
prod_fields = ["product_id", "product_name", "category", "brand", "cost_price", "list_price"]
cus_path = input_folder / "customers.csv"
prod_path = input_folder / "products.json"

try:
    validate_file_structure(cus_path, cus_fields)
    logger.info("customers.csv structure GOOD")
    validate_file_structure(prod_path, prod_fields)
    logger.info("products.json structure GOOD")

except DataValidationError as e:
    logger.error(str(e))
    raise SystemExit(1)

# --- Lab 2.4 ---
output_folder = Path(config["data_output"])
rejects_folder = Path(config["data_rejects"])

valid_customers, rejected_customers = validate_records(customers, id_field = "customer_id", date_fields = ["signup_date"])
valid_products, rejected_products = validate_records(products, id_field = "product_id", num_fields = ["cost_price", "list_price"])

logger.info(f"Customers: {len(valid_customers)} valid, {len(rejected_customers)} rejected")
if rejected_customers:
    logger.warning(f"{len(rejected_customers)} customer records rejected")

logger.info(f"Products: {len(valid_products)} valid, {len(rejected_products)} rejected")
if rejected_products:
    logger.warning(f"{len(rejected_products)} product records rejected")

with open(output_folder / "customers_valid.csv", "w", newline = "") as f:
    writer = csv.DictWriter(f, fieldnames = cus_fields)
    writer.writeheader()
    for row in valid_customers:
        writer.writerow({k: row[k] for k in cus_fields})

with open(rejects_folder / "customers_rejects.csv", "w", newline = "") as f:
    reject_fields = cus_fields + ["rejection_reason"]
    writer = csv.DictWriter(f, fieldnames = reject_fields)
    writer.writeheader()
    for row in rejected_customers:
        writer.writerow({k: row.get(k, "") for k in reject_fields})

with open(output_folder / "products_valid.json", "w") as f:
    json.dump(valid_products, f, indent = 2)

with open(rejects_folder / "products_rejects.json", "w") as f:
    json.dump(rejected_products, f, indent = 2)

logger.info("Pipeline finished")