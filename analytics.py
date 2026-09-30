
import pyodbc
import pandas as pd

# =====================================
# 1. SQL SERVER CONNECTION
# =====================================

server = r"localhost\SQLEXPRESS01"
database = "AIBusinessAnalystDB"

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)

print("Connected to SQL Server successfully!")


# =====================================
# 2. RETRIEVE SALES DATA
# =====================================

query = """
SELECT
    O.OrderID,
    O.OrderDate,
    O.OrderStatus,
    P.ProductName,
    P.Category,
    P.CostPrice,
    OD.Quantity,
    OD.UnitPrice,
    OD.DiscountAmount,

    (OD.Quantity * OD.UnitPrice)
        - OD.DiscountAmount AS Revenue,

    (OD.Quantity * P.CostPrice) AS TotalCost,

    (
        (OD.Quantity * OD.UnitPrice)
        - OD.DiscountAmount
        - (OD.Quantity * P.CostPrice)
    ) AS GrossProfit

FROM Orders O

JOIN OrderDetails OD
    ON O.OrderID = OD.OrderID

JOIN Products P
    ON OD.ProductID = P.ProductID

WHERE O.OrderStatus = 'Completed';
"""

df = pd.read_sql_query(query, connection)

connection.close()

print("\nSales data retrieved successfully!")


# =====================================
# 3. CALCULATE BUSINESS KPIs
# =====================================

total_revenue = df["Revenue"].sum()

total_cost = df["TotalCost"].sum()

gross_profit = df["GrossProfit"].sum()

total_orders = df["OrderID"].nunique()

total_units_sold = df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0 else 0
)


# =====================================
# 4. DISPLAY BUSINESS REPORT
# =====================================

print("\n" + "=" * 45)
print("       BUSINESS PERFORMANCE REPORT")
print("=" * 45)

print(f"Total Revenue:       Rs. {total_revenue:,.2f}")
print(f"Total Cost:          Rs. {total_cost:,.2f}")
print(f"Gross Profit:        Rs. {gross_profit:,.2f}")
print(f"Total Orders:        {total_orders}")
print(f"Units Sold:          {total_units_sold}")
print(f"Average Order Value: Rs. {average_order_value:,.2f}")


# =====================================
# 5. MONTHLY REVENUE
# =====================================

df["OrderDate"] = pd.to_datetime(df["OrderDate"])

df["Month"] = df["OrderDate"].dt.to_period("M")

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

print("\nMONTHLY REVENUE")
print(monthly_revenue.to_string(index=False))


# =====================================
# 6. CATEGORY-WISE REVENUE
# =====================================

category_revenue = (
    df.groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

print("\nCATEGORY-WISE REVENUE")
print(category_revenue.to_string())


# =====================================
# 7. TOP-SELLING PRODUCTS
# =====================================

top_products = (
    df.groupby("ProductName")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTOP-SELLING PRODUCTS")
print(top_products.to_string())


print("\nAnalytics completed successfully!")