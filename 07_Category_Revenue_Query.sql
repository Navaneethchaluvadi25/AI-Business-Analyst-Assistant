
USE AIBusinessAnalystDB;
GO

-- CUSTOMERS
INSERT INTO Customers
(CustomerName, Email, City, Region, CustomerType)
VALUES
('Rahul Sharma', 'rahul@email.com', 'Hyderabad', 'South', 'Regular'),
('Priya Reddy', 'priya@email.com', 'Bangalore', 'South', 'Premium'),
('Arjun Kumar', 'arjun@email.com', 'Chennai', 'South', 'Regular'),
('Sneha Patel', 'sneha@email.com', 'Mumbai', 'West', 'Premium'),
('Kiran Verma', 'kiran@email.com', 'Delhi', 'North', 'Regular');
GO

-- PRODUCTS
INSERT INTO Products
(ProductName, Category, CostPrice, SellingPrice, OpeningStock)
VALUES
('Classic T-Shirt', 'Menswear', 500, 1000, 100),
('Summer Dress', 'Womenswear', 900, 1800, 80),
('Running Sneakers', 'Footwear', 1200, 2500, 60),
('Leather Handbag', 'Accessories', 600, 1200, 50),
('Slim Fit Jeans', 'Menswear', 800, 1600, 90);
GO

-- ORDERS
INSERT INTO Orders
(CustomerID, OrderDate, OrderStatus)
VALUES
(1, '2025-01-05', 'Completed'),
(2, '2025-01-12', 'Completed'),
(3, '2025-01-20', 'Completed'),

(1, '2025-02-04', 'Completed'),
(2, '2025-02-14', 'Completed'),
(3, '2025-02-22', 'Completed'),

(1, '2025-03-03', 'Completed'),
(4, '2025-03-15', 'Completed'),
(5, '2025-03-25', 'Completed');
GO

-- ORDER DETAILS
INSERT INTO OrderDetails
(OrderID, ProductID, Quantity, UnitPrice, DiscountAmount)
VALUES
-- JANUARY
(1, 1, 5, 1000, 0),
(1, 5, 2, 1600, 0),
(2, 2, 3, 1800, 0),
(3, 3, 2, 2500, 0),

-- FEBRUARY
(4, 1, 4, 1000, 0),
(4, 5, 3, 1600, 0),
(5, 2, 2, 1800, 0),
(5, 4, 3, 1200, 0),
(6, 3, 3, 2500, 0),

-- MARCH
(7, 1, 2, 1000, 0),
(8, 2, 1, 1800, 0),
(8, 4, 1, 1200, 0),
(9, 5, 1, 1600, 0);
GO

-- INVENTORY TRANSACTIONS
INSERT INTO InventoryTransactions
(ProductID, TransactionDate, TransactionType, Quantity, Notes)
VALUES
(1, '2025-01-02', 'INWARD', 50, 'January stock arrival'),
(2, '2025-01-03', 'INWARD', 40, 'January stock arrival'),
(3, '2025-01-04', 'INWARD', 30, 'January stock arrival'),
(4, '2025-01-05', 'INWARD', 25, 'January stock arrival'),
(5, '2025-01-06', 'INWARD', 45, 'January stock arrival'),

(1, '2025-02-10', 'DAMAGE', 3, 'Damaged during handling'),
(3, '2025-02-12', 'DAMAGE', 2, 'Defective items'),
(5, '2025-03-10', 'INWARD', 20, 'March stock replenishment');
GO

-- MONTHLY SALES TARGETS
INSERT INTO SalesTargets
(TargetMonth, Category, RevenueTarget)
VALUES
('2025-01-01', 'Menswear', 15000),
('2025-01-01', 'Womenswear', 10000),
('2025-01-01', 'Footwear', 10000),

('2025-02-01', 'Menswear', 15000),
('2025-02-01', 'Womenswear', 10000),
('2025-02-01', 'Footwear', 10000),

('2025-03-01', 'Menswear', 15000),
('2025-03-01', 'Womenswear', 10000),
('2025-03-01', 'Footwear', 10000);
GO

PRINT 'Sample business data inserted successfully!';
GO