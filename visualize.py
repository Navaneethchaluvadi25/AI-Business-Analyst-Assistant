import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS01;"
    "Database=AIBusinessAnalystDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

connection = pyodbc.connect(connection_string)

# Monthly revenue
monthly_query = """
SELECT
    FORMAT(o.OrderDate, 'yyyy-MM') AS Month,
    SUM(od.Quantity * od.UnitPrice - od.DiscountAmount) AS Revenue
FROM dbo.Orders o
INNER JOIN dbo.OrderDetails od ON o.OrderID = od.OrderID
WHERE o.OrderStatus = 'Completed'
GROUP BY FORMAT(o.OrderDate, 'yyyy-MM')
ORDER BY Month;
"""

# Category revenue
category_query = """
SELECT
    p.Category,
    SUM(od.Quantity * od.UnitPrice - od.DiscountAmount) AS Revenue
FROM dbo.OrderDetails od
INNER JOIN dbo.Orders o ON od.OrderID = o.OrderID
INNER JOIN dbo.Products p ON od.ProductID = p.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.Category
ORDER BY Revenue DESC;
"""

# Top-selling products
products_query = """
SELECT
    p.ProductName,
    SUM(od.Quantity) AS UnitsSold
FROM dbo.OrderDetails od
INNER JOIN dbo.Orders o ON od.OrderID = o.OrderID
INNER JOIN dbo.Products p ON od.ProductID = p.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.ProductName
ORDER BY UnitsSold DESC;
"""

monthly_df = pd.read_sql_query(monthly_query, connection)
category_df = pd.read_sql_query(category_query, connection)
products_df = pd.read_sql_query(products_query, connection)

connection.close()

# Chart 1: Monthly revenue
plt.figure(figsize=(8, 5))
plt.plot(monthly_df["Month"], monthly_df["Revenue"], marker="o")
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (Rs.)")
plt.grid(True)
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.show()

# Chart 2: Category revenue
plt.figure(figsize=(8, 5))
plt.bar(category_df["Category"], category_df["Revenue"])
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (Rs.)")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("category_revenue.png")
plt.show()

# Chart 3: Top-selling products
plt.figure(figsize=(8, 5))
plt.bar(products_df["ProductName"], products_df["UnitsSold"])
plt.title("Units Sold by Product")
plt.xlabel("Product")
plt.ylabel("Units Sold")
plt.xticks(rotation=25)
plt.tight_layout()
plt.savefig("top_selling_products.png")
plt.show()

print("Charts generated successfully!")