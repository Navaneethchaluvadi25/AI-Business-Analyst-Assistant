import pyodbc

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

    print("Connection successful!")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            @@SERVERNAME,
            DB_NAME(),
            SUSER_SNAME()
    """)

    print("Connection details:", cursor.fetchone())

    cursor.close()
    conn.close()

except Exception as e:
    print("Connection failed!")
    print(e)