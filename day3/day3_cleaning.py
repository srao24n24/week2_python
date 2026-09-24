# -------- Cleaning Data --------
import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime
from cleaning_utils import(
    clean_customers,
    clean_products,
    clean_orders,
    clean_order_items,
    add_dataset_and_timestamp
)

with open("day3/config.json") as f:
    config = json.load(f)

# --- Lab 3.1 ---
input_folder = Path(config["data_input"])

def profile_dataset(df, file_name, id_col_name):
    print(f"\n----- {file_name} -----")
    print(df.shape)
    print("-----")
    print(df.dtypes)
    print("-----")
    print(df.isnull().sum())
    print("-----")
    print(df.duplicated(subset = [id_col_name]).sum())

cus_df = pd.read_csv(input_folder / "customers.csv")
profile_dataset(cus_df, "customers", "customer_id")

o_items_df = pd.read_csv(input_folder / "order_items.csv")
profile_dataset(o_items_df, "order items", "order_item_id")

order_df = pd.read_csv(input_folder / "orders.csv")
profile_dataset(order_df, "orders", "order_id")

prod_df = pd.read_json(input_folder / "products.json")
profile_dataset(prod_df, "products", "product_id")

# --- Lab 3.2 & 3.3 & 3.4 & 3.5 ---
output_folder = Path(config["data_output"])
rejects_folder = Path(config["data_rejects"])
output_folder.mkdir(parents = True, exist_ok = True)
rejects_folder.mkdir(parents = True, exist_ok = True)

valid_customers, rejected_customers = clean_customers(cus_df)
valid_products, rejected_products = clean_products(prod_df)
valid_orders, rejected_orders = clean_orders(order_df, valid_customers["customer_id"])
valid_order_items, rejected_order_items = clean_order_items(o_items_df, valid_orders["order_id"], valid_products["product_id"])
 
print("\n----- CLEANING SUMMARY -----")
print(f"Customers: {len(cus_df)} = {len(valid_customers)} valid + {len(rejected_customers)} rejected")
print(f"Products: {len(prod_df)} = {len(valid_products)} valid + {len(rejected_products)} rejected")
print(f"Orders: {len(order_df)} = {len(valid_orders)} valid + {len(rejected_orders)} rejected")
print(f"Order items: {len(o_items_df)} = {len(valid_order_items)} valid + {len(rejected_order_items)} rejected")
 
valid_customers.to_csv(output_folder / "clean_customers.csv", index = False)
valid_products.to_csv(output_folder / "clean_products.csv", index = False)
valid_orders.to_csv(output_folder / "clean_orders.csv", index = False)
valid_order_items.to_csv(output_folder / "clean_order_items.csv", index = False)

# --- Lab 3.6 ---
run_timestamp = datetime.now().isoformat()
 
rejected_customers = add_dataset_and_timestamp(rejected_customers, "customers", run_timestamp)
rejected_products = add_dataset_and_timestamp(rejected_products, "products", run_timestamp)
rejected_orders = add_dataset_and_timestamp(rejected_orders, "orders", run_timestamp)
rejected_order_items = add_dataset_and_timestamp(rejected_order_items, "order_items", run_timestamp)
 
all_rejects = pd.concat([rejected_customers, rejected_products, rejected_orders, rejected_order_items], ignore_index = True)
all_rejects.to_csv(rejects_folder / "all_rejects.csv", index = False)
 
print(f"\nTotal rejects across all datasets: {len(all_rejects)}")

# --- Lab 3.7 ---
def build_quality_row(dataset_name, input_df, valid_df, rejected_df):
    return {
        "dataset": dataset_name, "input_count": len(input_df), "valid_count": len(valid_df), "rejected_count": len(rejected_df),
        "duplicate_count": rejected_df["rejection_reason"].str.contains("duplicate").sum(),
        "missing_key_count": rejected_df["rejection_reason"].str.contains("missing").sum()
    }
 
quality_rows = [
    build_quality_row("customers", cus_df, valid_customers, rejected_customers),
    build_quality_row("products", prod_df, valid_products, rejected_products),
    build_quality_row("orders", order_df, valid_orders, rejected_orders),
    build_quality_row("order_items", o_items_df, valid_order_items, rejected_order_items)
]
 
data_quality_report = pd.DataFrame(quality_rows)
data_quality_report.to_csv(output_folder / "data_quality_report.csv", index = False)
 
print("\n----- DATA QUALITY REPORT -----")
print(data_quality_report.to_string(index = False))
 
