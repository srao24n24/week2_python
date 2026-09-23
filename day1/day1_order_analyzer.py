# --- Order Analyzer ---
from sales_utils import (
    calculate_line_total,
    calculate_order_total,
    get_delivery_status,
    classify_order,
    get_unique_products,
    get_product_quantities,
    get_high_value_products,
)

# ---------- Given Info ----------
order_items = [
    ("Laptop", 2, 45000),
    ("Mouse", 3, 800),
    ("Laptop", 1, 45000),
    ("Keyboard", 2, 1500),
]
discount_percentage = 10
# --------------------------------

line_total = []
total_quantity, gross_value, discount_amount, net_value = calculate_order_total(order_items, discount_percentage)
delivery_status = get_delivery_status(net_value)
order_classification = classify_order(net_value)
unique_products = get_unique_products(order_items)
product_total_quantity = get_product_quantities(order_items, unique_products)
high_value_products = get_high_value_products(order_items)

summary = {
    "gross value": gross_value, "discount": discount_amount, "net value": net_value, "classification": order_classification,
    "delivery status": delivery_status, "unique products": unique_products,
}

for product, quantity, unit_price in order_items:
    line_total.append(calculate_line_total(quantity, unit_price))

# ---------- Output ----------
print("\n-------- RETAIL ORDER SUMMARY --------")

print(F"\nLine Totals: {line_total}")
print(f"Total Quantity: {total_quantity}")
print(f"Gross Value: {gross_value:.2f}")
print(f"Discount: {discount_amount:.2f}")
print(f"Net Value: {net_value:.2f}")
print(f"Classification: {order_classification}")
print(f"Delivery Status: {delivery_status}")
print(f"Unique Products: {unique_products}")
print(f"High-Value Products: {high_value_products}")
print(f"Consolidated Product Quantities: {product_total_quantity}")

print("\n--------------------------------------")
