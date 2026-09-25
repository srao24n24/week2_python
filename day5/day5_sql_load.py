# -------- SQL Load --------
import os
from dotenv import load_dotenv
import pyodbc
import uuid
import pandas as pd
from datetime import datetime

# --- Lab 5.1 ---
load_dotenv("day5/.env", encoding="utf-8-sig")

server = os.environ["DB_SERVER"]
database = os.environ["DB_NAME"]

conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

conn = pyodbc.connect(conn_str)
print("Connected successfully!")

# --- Lab 5.3 ---
# NOTE: Did not know what to do for batch_id varchar(36) so asked AI to help me do this and understand
batch_id = str(uuid.uuid4())
start_time = datetime.now()

fact_df = pd.read_csv("day4/data/output/fact_sales.csv")
fact_df = fact_df.rename(columns = {"gross": "gross_sales", "discount": "discount_amount", "net": "net_sales", "cost": "total_cost", "profit": "gross_profit"})

stage_columns = ["order_item_id", "order_id", "customer_id", "product_id", "order_date", "quantity", "unit_price", "discount_pct", "gross_sales", "discount_amount", "net_sales", "total_cost", "gross_profit"]

stage_df = fact_df[stage_columns].copy()
stage_df.insert(0, "batch_id", batch_id)

cursor = conn.cursor()
cursor.fast_executemany = True

insert_sql = f"""
    INSERT INTO dbo.stg_fact_sales({', '.join(stage_columns)}, batch_id) VALUES ({', '.join(['?'] * len(stage_columns))}, ?)
"""

rows_to_insert = [tuple(row[col] for col in stage_columns) + (batch_id,) for _, row in stage_df.iterrows()]

cursor.executemany(insert_sql, rows_to_insert)
conn.commit()

print(f"Loaded {len(rows_to_insert)} rows into stg_fact_sales with batch_id {batch_id}")

# --- Lab 5.4 + 5.5 ---
cursor.execute("SELECT COUNT(*) FROM dbo.fact_sales")
result = cursor.fetchone()
before_count = result[0]

try:
    insert_sql = """
        INSERT INTO dbo.fact_sales (order_item_id, order_id, customer_id, product_id, order_date, quantity, unit_price, discount_pct, gross_sales, discount_amount, net_sales, total_cost, gross_profit, last_batch_id)
        SELECT order_item_id, order_id, customer_id, product_id, order_date, quantity, unit_price, discount_pct, gross_sales, discount_amount, net_sales, total_cost, gross_profit, batch_id
        FROM dbo.stg_fact_sales
        WHERE batch_id = ? AND NOT EXISTS (SELECT 1 FROM dbo.fact_sales WHERE fact_sales.order_item_id = stg_fact_sales.order_item_id)
    """

    cursor.execute(insert_sql, (batch_id,))
    loaded_rows = cursor.rowcount
    conn.commit()
    print("Transaction successful. Changes committed.")

except Exception as e:
    conn.rollback()
    loaded_rows = 0
    print("Transaction failed.")
    print("Changes rolled back.")
    print(e)

cursor.execute("SELECT COUNT(*) FROM dbo.fact_sales")
result = cursor.fetchone()
after_count = result[0]

print(f"Before: {before_count}")
print(f"After: {after_count}")
print(f"Loaded: {loaded_rows}")

# --- Lab 5.6 ---
input_rows = len(fact_df)
valid_rows = len(stage_df)
rejected_rows = 0
source_name = "fact_sales.csv"
end_time = datetime.now()
status = "SUCCESS"
error_message = None

if loaded_rows == 0:
    status = "SUCCESS"

cursor = conn.cursor()

audit_sql = """
    INSERT INTO dbo.etl_batch_log(batch_id, started_at, ended_at, source_name, input_rows, valid_rows, rejected_rows, loaded_rows, status, error_message)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

cursor.execute(
    audit_sql, (batch_id, start_time, end_time, source_name, input_rows, valid_rows, rejected_rows, loaded_rows, status, error_message)
)

conn.commit()
print("Audit log done successfully.")

# --- Lab 5.7 ---
source_count = len(fact_df)
source_net_sales = fact_df["net_sales"].sum()
source_unique_order_items = fact_df["order_item_id"].nunique()

cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*), SUM(net_sales), COUNT(DISTINCT order_item_id)
    FROM dbo.fact_sales
""")

result = cursor.fetchone()

target_count = result[0]
target_net_sales = result[1]
target_unique_order_items = result[2]

reconciliation = pd.DataFrame([
    {"check": "row_count", "source_value": source_count, "target_value": target_count, "status": "Match" if source_count == target_count else "Mismatch"},
    {"check": "net_sales", "source_value": source_net_sales, "target_value": target_net_sales, "status": "Match" if source_net_sales == target_net_sales else "Mismatch"},
    {"check": "unique_order_item_id", "source_value": source_unique_order_items, "target_value": target_unique_order_items, "status": "Match" if source_unique_order_items == target_unique_order_items else "Mismatch"}
])

reconciliation.to_csv("day5/data/output/load_reconciliation.csv", index = False)

print("\n--- Reconciliation ---")
print(f"Source rows: {source_count}")
print(f"Target rows: {target_count}")
print(f"Source net sales: {source_net_sales}")
print(f"Target net sales: {target_net_sales}")
print(f"Source unique order items: {source_unique_order_items}")
print(f"Target unique order items: {target_unique_order_items}")
print(f"Count match: {source_count == target_count}")
print(f"Net sales match: {source_net_sales == target_net_sales}")
print(f"Unique order item match: {source_unique_order_items == target_unique_order_items}")

conn.close()