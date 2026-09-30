
USE AIBusinessAnalystDB;
GO

SELECT
    TABLE_NAME,
    COLUMN_NAME,
    DATA_TYPE,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME IN (
    'Customers',
    'Products',
    'Orders',
    'OrderDetails',
    'InventoryTransactions',
    'SalesTargets'
)
ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO