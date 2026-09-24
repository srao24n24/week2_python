# --- Cleaning Utils ---
import pandas as pd

def clean_customers(df):
    df = df.copy()
    df["customer_name"] = df["customer_name"].str.strip().str.title()
    df["email"] = df["email"].str.strip().str.lower()
    df["city"] = df["city"].str.strip().str.title()
    df["state"] = df["state"].str.strip().str.title()
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors = "coerce")

    rejection_mask = (df["customer_id"].isnull() | df["customer_id"].duplicated(keep = "first") | df["signup_date"].isnull())

    rejected_df = df[rejection_mask]
    valid_df = df[~ rejection_mask]
    valid_df["customer_id"] = valid_df["customer_id"].astype(int)
    
    return valid_df, rejected_df

def clean_products(df):
    df = df.copy()
    df["product_id"] = pd.to_numeric(df["product_id"], errors = "coerce")
    df["cost_price"] = df["cost_price"].astype(float)

    rejection_mask = ((df["product_id"].isnull()) | (df["cost_price"] > df["list_price"]) | df["product_id"].duplicated(keep = "first"))

    rejected_df = df[rejection_mask]
    valid_df = df[~ rejection_mask]
    valid_df["product_id"] = valid_df["product_id"].astype(int)

    return valid_df, rejected_df

def clean_orders(df, valid_customer_ids):
    accepted_order_status = ["Placed", "Paid", "Shipped", "Delivered", "Cancelled"]
    accepted_channels = ["Web", "Mobile", "Store"]
    df = df.copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors = "coerce")

    rejection_mask = ((~df["order_status"].isin(accepted_order_status)) | (~df["sales_channel"].isin(accepted_channels)) | 
                      (~df["customer_id"].isin(valid_customer_ids)) | (df["order_id"].duplicated(keep = "first")) | (df["order_date"].isnull()))
    
    rejected_df = df[rejection_mask]
    valid_df = df[~ rejection_mask]
    
    return valid_df, rejected_df

def clean_order_items(df, valid_order_ids, valid_product_ids):
    df = df.copy()
    df["order_item_id"] = pd.to_numeric(df["order_item_id"], errors = "coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors = "coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors = "coerce")
    df["discount_pct"] = pd.to_numeric(df["discount_pct"], errors = "coerce")

    rejection_mask = ((df["order_item_id"].isnull()) | (df["order_item_id"].duplicated(keep="first")) | (df["quantity"].isnull()) | 
                      (df["quantity"] <= 0) | (df["unit_price"].isnull()) | (df["unit_price"] < 0) | (df["discount_pct"].isnull()) | 
                      (df["discount_pct"] < 0) | (df["discount_pct"] > 100) | (~df["order_id"].isin(valid_order_ids)) | (~df["product_id"].isin(valid_product_ids))
    )

    rejected_df = df[rejection_mask]
    valid_df = df[~rejection_mask]
    valid_df["order_item_id"] = valid_df["order_item_id"].astype(int)

    return valid_df, rejected_df