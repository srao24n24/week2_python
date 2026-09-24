# -------- Data Transformation --------
import pandas as pd
import json
from pathlib import Path

with open("day4/config.json") as f:
    config = json.load(f)

input_folder = Path(config["data_input"])
output_folder = Path(config["data_output"])

# --- Lab 4.1 ---
clean_cus_df = pd.read_csv(input_folder / "clean_customers.csv")
clean_o_items_df = pd.read_csv(input_folder / "clean_order_items.csv")
clean_order_df = pd.read_csv(input_folder / "clean_orders.csv")
clean_prod_df = pd.read_csv(input_folder / "clean_products.csv")

cus_order_df = clean_order_df.merge(clean_cus_df, how = "inner", on = "customer_id")
order_o_item_df = clean_o_items_df.merge(cus_order_df, how = "inner", on = "order_id")
prod_o_item_df = order_o_item_df.merge(clean_prod_df, how = "inner", on = "product_id")

fact_sales_df = prod_o_item_df[prod_o_item_df["order_status"] != "Cancelled"]

# --- Lab 4.2 ---
fact_sales_df["gross"] = fact_sales_df["quantity"] * fact_sales_df["unit_price"]
fact_sales_df["discount"] = fact_sales_df["gross"] * (fact_sales_df["discount_pct"] / 100)
fact_sales_df["net"] = fact_sales_df["gross"] - fact_sales_df["discount"]
fact_sales_df["cost"] = fact_sales_df["quantity"] * fact_sales_df["cost_price"]
fact_sales_df["profit"] = fact_sales_df["net"] - fact_sales_df["cost"]
fact_sales_df["margin_pct"] = round((fact_sales_df["profit"] / fact_sales_df["net"]) * 100, 2)

fact_sales_df.to_csv(output_folder / "fact_sales.csv", index = False)

# --- Lab 4.3 ---



