import pyodbc

connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=localhost\\SQLEXPRESS01;"
    "Database=AIBusinessAnalystDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Orders")
    order_count = cursor.fetchone()[0]

    print("SQL Server connection successful!")
    print(f"Orders found in database: {order_count}")

    connection.close()

except Exception as error:
    print("Database connection failed:")
    print(error)