SELECT
    @@SERVERNAME AS ServerName,
    DB_NAME() AS CurrentDatabase,
    SUSER_SNAME() AS LoginName;

SELECT
    name,
    state_desc,
    SUSER_SNAME(owner_sid) AS DatabaseOwner
FROM sys.databases
WHERE name = 'ABusinessAnalystDB';