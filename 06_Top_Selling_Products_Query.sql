USE AIBusinessAnalystDB;
GO

-- 1. CUSTOMERS
CREATE TABLE Customers
(
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(100) NOT NULL,
    Email VARCHAR(150),
    City VARCHAR(100),
    Region VARCHAR(100),
    CustomerType VARCHAR(30) DEFAULT 'Regular'
);
GO

-- 2. PRODUCTS
CREATE TABLE Products
(
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    CostPrice DECIMAL(10,2) NOT NULL,
    SellingPrice DECIMAL(10,2) NOT NULL,
    OpeningStock INT NOT NULL DEFAULT 0,

    CONSTRAINT CK_Products_Cost
        CHECK (CostPrice >= 0),

    CONSTRAINT CK_Products_Price
        CHECK (SellingPrice >= 0),

    CONSTRAINT CK_Products_Stock
        CHECK (OpeningStock >= 0)
);
GO

-- 3. ORDERS
CREATE TABLE Orders
(
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    OrderDate DATE NOT NULL,
    OrderStatus VARCHAR(30) NOT NULL DEFAULT 'Completed',

    CONSTRAINT FK_Orders_Customers
        FOREIGN KEY (CustomerID)
        REFERENCES Customers(CustomerID)
);
GO

-- 4. ORDER DETAILS
CREATE TABLE OrderDetails
(
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    UnitPrice DECIMAL(10,2) NOT NULL,
    DiscountAmount DECIMAL(10,2) NOT NULL DEFAULT 0,

    CONSTRAINT FK_OrderDetails_Orders
        FOREIGN KEY (OrderID)
        REFERENCES Orders(OrderID),

    CONSTRAINT FK_OrderDetails_Products
        FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID),

    CONSTRAINT CK_OrderDetails_Quantity
        CHECK (Quantity > 0),

    CONSTRAINT CK_OrderDetails_Price
        CHECK (UnitPrice >= 0),

    CONSTRAINT CK_OrderDetails_Discount
        CHECK (DiscountAmount >= 0)
);
GO

-- 5. INVENTORY TRANSACTIONS
CREATE TABLE InventoryTransactions
(
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    ProductID INT NOT NULL,
    TransactionDate DATE NOT NULL,
    TransactionType VARCHAR(20) NOT NULL,
    Quantity INT NOT NULL,
    Notes VARCHAR(255),

    CONSTRAINT FK_InventoryTransactions_Products
        FOREIGN KEY (ProductID)
        REFERENCES Products(ProductID),

    CONSTRAINT CK_InventoryTransactions_Type
        CHECK (TransactionType IN
        ('INWARD', 'DAMAGE', 'ADJUSTMENT')),

    CONSTRAINT CK_InventoryTransactions_Quantity
        CHECK (Quantity > 0)
);
GO

-- 6. MONTHLY SALES TARGETS
CREATE TABLE SalesTargets
(
    TargetID INT IDENTITY(1,1) PRIMARY KEY,
    TargetMonth DATE NOT NULL,
    Category VARCHAR(50),
    RevenueTarget DECIMAL(12,2) NOT NULL,

    CONSTRAINT CK_SalesTargets_Revenue
        CHECK (RevenueTarget >= 0)
);
GO

-- VERIFY TABLES
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO