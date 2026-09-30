-- Check SQL Server connection and database

SELECT
    @@SERVERNAME AS ServerName,
    DB_NAME() AS CurrentDatabase,
    SUSER_SNAME() AS LoginName;
GO

-- Check whether the project database exists and is online

SELECT
    name AS DatabaseName,
    state_desc AS DatabaseStatus
FROM sys.databases
WHERE name = 'AIBusinessAnalystDB';
GO