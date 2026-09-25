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

fact_sales_df = prod_o_item_df[prod_o_item_df["order_status"] != "Cancelled"].copy()

# --- Lab 4.2 ---
fact_sales_df["gross"] = fact_sales_df["quantity"] * fact_sales_df["unit_price"]
fact_sales_df["discount"] = fact_sales_df["gross"] * (fact_sales_df["discount_pct"] / 100)
fact_sales_df["net"] = fact_sales_df["gross"] - fact_sales_df["discount"]
fact_sales_df["cost"] = fact_sales_df["quantity"] * fact_sales_df["cost_price"]
fact_sales_df["profit"] = fact_sales_df["net"] - fact_sales_df["cost"]
fact_sales_df["margin_pct"] = round((fact_sales_df["profit"] / fact_sales_df["net"]) * 100, 2)

fact_sales_df.to_csv(output_folder / "fact_sales.csv", index = False)

# --- Lab 4.3 ---
customer_summary = fact_sales_df.groupby("customer_id").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()
product_summary = fact_sales_df.groupby("product_id").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()
category_summary = fact_sales_df.groupby("category").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()
state_summary = fact_sales_df.groupby("state").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()
channel_summary = fact_sales_df.groupby("sales_channel").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()

fact_sales_df["month"] = pd.to_datetime(fact_sales_df["order_date"]).dt.to_period("M")
monthly_summary = fact_sales_df.groupby("month").agg(total_net_sales = ("net", "sum"), total_profit = ("profit", "sum"), total_quantity = ("quantity", "sum")).reset_index()

customer_summary.to_csv(output_folder / "customer_summary.csv", index = False)
product_summary.to_csv(output_folder / "product_summary.csv", index = False)
category_summary.to_csv(output_folder / "category_summary.csv", index = False)
state_summary.to_csv(output_folder / "state_summary.csv", index = False)
channel_summary.to_csv(output_folder / "channel_summary.csv", index = False)
monthly_summary.to_csv(output_folder / "monthly_summary.csv", index = False)

# --- Lab 4.4 ---
customer_summary["rank"] = customer_summary["total_net_sales"].rank(method = "min", ascending = False)
product_summary["rank"] = product_summary["total_net_sales"].rank(method = "min", ascending = False)
prod_cat = fact_sales_df.groupby(["category", "product_id"]).agg(total_net_sales = ("net", "sum")).reset_index()
prod_cat["rank"] = prod_cat.groupby("category")["total_net_sales"].rank(method = "min", ascending = False)

top_10_cus = customer_summary.sort_values("rank").head(10)
top_10_prod = product_summary.sort_values("rank").head(10)
top_3_prod_cat = (prod_cat.sort_values(["category", "rank"]).groupby("category").head(3))

top_10_cus.to_csv(output_folder / "top_10_customers.csv", index = False)
top_10_prod.to_csv(output_folder / "top_10_products.csv", index = False)
top_3_prod_cat.to_csv(output_folder / "top_3_products_category.csv", index = False)

# --- Lab 4.5 ---
monthly_summary = monthly_summary.sort_values("month")
monthly_summary["previous_month_sales"] = monthly_summary["total_net_sales"].shift(1)
monthly_summary["month_over_month_growth"] = ((monthly_summary["total_net_sales"] - monthly_summary["previous_month_sales"]) / monthly_summary["previous_month_sales"]) * 100

monthly_summary.to_csv(output_folder / "monthly_sales.csv", index = False)

# --- Lab 4.6 ---
cat_month_pivot = pd.pivot_table(fact_sales_df, index = "category", columns = "month", values = "net", aggfunc = "sum")
cat_month_pivot.to_csv(output_folder / "category_month_pivot.csv", index = True)
print(cat_month_pivot)

# --- Lab 4.7 ---
duplicate_order_items = fact_sales_df["order_item_id"].duplicated().sum()
fact_row_count = len(fact_sales_df)
non_cancelled_orders = clean_order_df[clean_order_df["order_status"] != "Cancelled"]
expected_row_count = len(clean_o_items_df[clean_o_items_df["order_id"].isin(non_cancelled_orders["order_id"])])
detail_revenue = fact_sales_df["net"].sum()
summary_revenue = customer_summary["total_net_sales"].sum()

reconciliation_report = pd.DataFrame({
    "check": [
        "Duplicate order_item_id",
        "Fact row count",
        "Expected row count",
        "Detail revenue",
        "Summary revenue"
    ],
    "value": [
        duplicate_order_items,
        fact_row_count,
        expected_row_count,
        detail_revenue,
        summary_revenue
    ]
})

reconciliation_report.to_csv(output_folder / "reconciliation_report.csv", index = False)
print(reconciliation_report)

