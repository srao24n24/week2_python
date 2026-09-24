# -------- Cleaning Data --------
import json
import csv
import pandas as pd
from pathlib import Path
from cleaning_utils import(
    clean_customers,
    clean_products,
    clean_orders,
    clean_order_items
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

# --- Lab 3.2 ---


