
import pyodbc
import pandas as pd

# SQL Server connection
server = r"localhost\SQLEXPRESS01"
database = "AIBusinessAnalystDB"
driver = "ODBC Driver 18 for SQL Server"

connection_string = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    conn = pyodbc.connect(connection_string)

    print("Connected to SQL Server successfully!\n")

    # Get all user tables
    query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        AND TABLE_SCHEMA = 'dbo'
        ORDER BY TABLE_NAME;
    """

    tables = pd.read_sql_query(query, conn)

    print("DATABASE TABLES:")
    print(tables.to_string(index=False))

    print("\nTABLE DETAILS:")

    for table_name in tables["TABLE_NAME"]:

        print("\n" + "=" * 50)
        print(f"TABLE: {table_name}")
        print("=" * 50)

        # Retrieve table data
        df = pd.read_sql_query(
            f"SELECT * FROM dbo.[{table_name}]",
            conn
        )

        print("Total Records:", len(df))
        print("Columns:", list(df.columns))

        print("\nSample Data:")
        print(df.head().to_string(index=False))

    conn.close()

    print("\nDatabase inspection completed!")

except Exception as e:
    print("Error:", e)