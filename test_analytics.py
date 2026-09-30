from business_data import (
    get_sales_summary,
    get_inventory_summary,
    get_monthly_revenue,
    get_category_revenue,
    get_top_selling_products
)

print("\n========== SALES SUMMARY ==========")
print(get_sales_summary())

print("\n========== INVENTORY SUMMARY ==========")
for item in get_inventory_summary():
    print(item)

print("\n========== MONTHLY REVENUE ==========")
for item in get_monthly_revenue():
    print(item)

print("\n========== CATEGORY REVENUE ==========")
for item in get_category_revenue():
    print(item)

print("\n========== TOP-SELLING PRODUCTS ==========")
for item in get_top_selling_products():
    print(item)