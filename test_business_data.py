from business_data import get_sales_summary, get_inventory_summary

print("SALES SUMMARY")
print(get_sales_summary())

print("\nINVENTORY SUMMARY")
for product in get_inventory_summary():
    print(product)