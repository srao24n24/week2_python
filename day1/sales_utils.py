# --- Sales Utils ---
def calculate_line_total(quantity, unit_price):
    return quantity * unit_price

def calculate_discount(gross_value, discount_percentage):
    return gross_value * (discount_percentage / 100)

def calculate_order_total(order_items, discount_percentage):
    total_quantity = 0
    gross_order_value = 0
    for product, quantity, unit_price in order_items:
        total_quantity += quantity
        gross_order_value += calculate_line_total(quantity, unit_price)
    discount_amount = calculate_discount(gross_order_value, discount_percentage)
    net_order_value = gross_order_value - discount_amount
    return total_quantity, gross_order_value, discount_amount, net_order_value

def get_delivery_status(net_order_value):
    if net_order_value >= 5000:
        return "Free Delivery"
    else:
        return "Delivery Charge Applicable"

def classify_order(net_value):
    if net_value < 2000:
        return "Small"
    elif net_value < 5000:
        return "Medium"
    else:
        return "Large"

def get_unique_products(order_items):
    products = set()
    for product, quantity, unit_price in order_items:
        products.add(product)
    return products

def get_product_quantities(order_items, unique_products):
    return {product: sum(qty for p, qty, price in order_items if p == product) for product in unique_products}

def get_high_value_products(order_items, threshold = 1000):
    return [product for product, quantity, unit_price in order_items if calculate_line_total(quantity, unit_price) > threshold]
