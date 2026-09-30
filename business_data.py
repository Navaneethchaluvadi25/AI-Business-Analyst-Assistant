import pyodbc


# ============================================================
# SQL SERVER CONNECTION
# ============================================================

CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS01;"
    "Database=AIBusinessAnalystDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


# ============================================================
# 1. SALES SUMMARY
# ============================================================

def get_sales_summary():

    query = """
        SELECT
            SUM(od.Quantity * od.UnitPrice - od.DiscountAmount)
                AS TotalRevenue,

            SUM(od.Quantity * p.CostPrice)
                AS TotalCost,

            SUM(
                od.Quantity * od.UnitPrice
                - od.DiscountAmount
                - od.Quantity * p.CostPrice
            ) AS GrossProfit,

            SUM(od.Quantity) AS TotalUnitsSold,

            COUNT(DISTINCT o.OrderID) AS TotalOrders

        FROM Orders o
        INNER JOIN OrderDetails od
            ON o.OrderID = od.OrderID
        INNER JOIN Products p
            ON od.ProductID = p.ProductID

        WHERE o.OrderStatus = 'Completed';
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        row = cursor.fetchone()

    return {
        "total_revenue": float(row.TotalRevenue or 0),
        "total_cost": float(row.TotalCost or 0),
        "gross_profit": float(row.GrossProfit or 0),
        "total_units_sold": int(row.TotalUnitsSold or 0),
        "total_orders": int(row.TotalOrders or 0),
    }


# ============================================================
# 2. INVENTORY SUMMARY
# ============================================================

def get_inventory_summary():

    query = """
        SELECT
            p.ProductName,

            p.OpeningStock
                + COALESCE(
                    SUM(
                        CASE
                            WHEN it.TransactionType = 'INWARD'
                                THEN it.Quantity

                            WHEN it.TransactionType = 'DAMAGE'
                                THEN -it.Quantity

                            ELSE 0
                        END
                    ), 0
                )
                - COALESCE(sold.UnitsSold, 0)
                AS RemainingStock

        FROM Products p

        LEFT JOIN InventoryTransactions it
            ON p.ProductID = it.ProductID

        LEFT JOIN (
            SELECT
                od.ProductID,
                SUM(od.Quantity) AS UnitsSold

            FROM OrderDetails od
            INNER JOIN Orders o
                ON od.OrderID = o.OrderID

            WHERE o.OrderStatus = 'Completed'

            GROUP BY od.ProductID
        ) sold
            ON p.ProductID = sold.ProductID

        GROUP BY
            p.ProductID,
            p.ProductName,
            p.OpeningStock,
            sold.UnitsSold

        ORDER BY RemainingStock ASC;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return [
        {
            "product": row.ProductName,
            "remaining_stock": int(row.RemainingStock or 0),
        }
        for row in rows
    ]


# ============================================================
# 3. MONTHLY REVENUE
# ============================================================

def get_monthly_revenue():

    query = """
        SELECT
            YEAR(o.OrderDate) AS SalesYear,
            MONTH(o.OrderDate) AS SalesMonth,

            SUM(
                od.Quantity * od.UnitPrice - od.DiscountAmount
            ) AS MonthlyRevenue

        FROM Orders o
        INNER JOIN OrderDetails od
            ON o.OrderID = od.OrderID

        WHERE o.OrderStatus = 'Completed'

        GROUP BY
            YEAR(o.OrderDate),
            MONTH(o.OrderDate)

        ORDER BY
            SalesYear,
            SalesMonth;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    month_names = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    return [
        {
            "month": f"{month_names[row.SalesMonth - 1]} {row.SalesYear}",
            "revenue": float(row.MonthlyRevenue or 0),
        }
        for row in rows
    ]


# ============================================================
# 4. CATEGORY-WISE REVENUE
# ============================================================

def get_category_revenue():

    query = """
        SELECT
            p.Category,

            SUM(
                od.Quantity * od.UnitPrice - od.DiscountAmount
            ) AS CategoryRevenue

        FROM Orders o
        INNER JOIN OrderDetails od
            ON o.OrderID = od.OrderID
        INNER JOIN Products p
            ON od.ProductID = p.ProductID

        WHERE o.OrderStatus = 'Completed'

        GROUP BY p.Category

        ORDER BY CategoryRevenue DESC;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return [
        {
            "category": row.Category,
            "revenue": float(row.CategoryRevenue or 0),
        }
        for row in rows
    ]


# ============================================================
# 5. TOP-SELLING PRODUCTS
# ============================================================

def get_top_selling_products():

    query = """
        SELECT TOP 5
            p.ProductName,

            SUM(od.Quantity) AS UnitsSold,

            SUM(
                od.Quantity * od.UnitPrice - od.DiscountAmount
            ) AS ProductRevenue

        FROM Orders o
        INNER JOIN OrderDetails od
            ON o.OrderID = od.OrderID
        INNER JOIN Products p
            ON od.ProductID = p.ProductID

        WHERE o.OrderStatus = 'Completed'

        GROUP BY
            p.ProductID,
            p.ProductName

        ORDER BY
            UnitsSold DESC,
            ProductRevenue DESC;
    """

    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

    return [
        {
            "product": row.ProductName,
            "units_sold": int(row.UnitsSold or 0),
            "revenue": float(row.ProductRevenue or 0),
        }
        for row in rows
    ]