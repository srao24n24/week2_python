# --- Cleaning Utils ---
# NOTE: I did not know how to implement the reason text (Lab 3.6) so AI was used to help me implement that part using np.where.
# That is why its so different then the previous commit
import pandas as pd
import numpy as np

def clean_customers(df):
    df = df.copy()
    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    df["city"] = df["city"].str.strip().str.title()
    df["state"] = df["state"].str.strip().str.title()
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    reason = pd.Series("", index=df.index)
    reason += np.where(df["customer_id"].isnull(), "missing customer_id; ", "")
    reason += np.where(df["customer_id"].duplicated(keep="first"), "duplicate customer_id; ", "")
    reason += np.where(df["signup_date"].isnull(), "invalid signup_date; ", "")
    reason = reason.str.rstrip("; ")

    rejection_mask = reason != ""  

    rejected_df = df[rejection_mask].copy()
    rejected_df["rejection_reason"] = reason[rejection_mask]

    valid_df = df[~rejection_mask].copy()
    valid_df["customer_id"] = valid_df["customer_id"].astype(int)

    return valid_df, rejected_df

def clean_products(df):
    df = df.copy()
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")
    df["cost_price"] = df["cost_price"].astype(float)

    reason = pd.Series("", index=df.index)
    reason += np.where(df["product_id"].isnull(), "missing product_id; ", "")
    reason += np.where(df["product_id"].duplicated(keep="first"), "duplicate product_id; ", "")
    reason += np.where(df["cost_price"] > df["list_price"], "cost_price greater than list_price; ", "")
    reason = reason.str.rstrip("; ")

    rejection_mask = reason != ""

    rejected_df = df[rejection_mask].copy()
    rejected_df["rejection_reason"] = reason[rejection_mask]

    valid_df = df[~rejection_mask].copy()
    valid_df["product_id"] = valid_df["product_id"].astype(int)

    return valid_df, rejected_df

def clean_orders(df, valid_customer_ids):
    accepted_order_status = ["Placed", "Paid", "Shipped", "Delivered", "Cancelled"]
    accepted_channels = ["Web", "Mobile", "Store"]
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    reason = pd.Series("", index=df.index)
    reason += np.where(df["order_id"].isnull(), "missing order_id; ", "")
    reason += np.where(df["order_id"].duplicated(keep="first"), "duplicate order_id; ", "")
    reason += np.where(df["order_date"].isnull(), "invalid order_date; ", "")
    reason += np.where(~df["order_status"].isin(accepted_order_status), "invalid order_status; ", "")
    reason += np.where(~df["sales_channel"].isin(accepted_channels), "invalid sales_channel; ", "")
    reason += np.where(~df["customer_id"].isin(valid_customer_ids), "unknown customer_id; ", "")
    reason = reason.str.rstrip("; ")

    rejection_mask = reason != ""

    rejected_df = df[rejection_mask].copy()
    rejected_df["rejection_reason"] = reason[rejection_mask]

    valid_df = df[~rejection_mask].copy()

    return valid_df, rejected_df

def clean_order_items(df, valid_order_ids, valid_product_ids):
    df = df.copy()
    df["order_item_id"] = pd.to_numeric(df["order_item_id"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors="coerce")

    reason = pd.Series("", index=df.index)
    reason += np.where(df["order_item_id"].isnull(), "missing order_item_id; ", "")
    reason += np.where(df["order_item_id"].duplicated(keep="first"), "duplicate order_item_id; ", "")
    reason += np.where(df["quantity"].isnull() | (df["quantity"] <= 0), "invalid quantity; ", "")
    reason += np.where(df["unit_price"].isnull() | (df["unit_price"] < 0), "invalid unit_price; ", "")
    reason += np.where(
        df["discount_pct"].isnull() | (df["discount_pct"] < 0) | (df["discount_pct"] > 100),
        "invalid discount_pct; ", ""
    )
    reason += np.where(~df["order_id"].isin(valid_order_ids), "unknown order_id; ", "")
    reason += np.where(~df["product_id"].isin(valid_product_ids), "unknown product_id; ", "")
    reason = reason.str.rstrip("; ")

    rejection_mask = reason != ""

    rejected_df = df[rejection_mask].copy()
    rejected_df["rejection_reason"] = reason[rejection_mask]

    valid_df = df[~rejection_mask].copy()
    valid_df["order_item_id"] = valid_df["order_item_id"].astype(int)

    return valid_df, rejected_df

def add_dataset_and_timestamp(rejected_df, dataset_name, run_timestamp):
    rejected_df = rejected_df.copy()
    rejected_df["dataset"] = dataset_name
    rejected_df["validation_timestamp"] = run_timestamp
    return rejected_df