SELECT
    p.ProductName,
    p.Category,
    SUM(od.Quantity) AS UnitsSold,
    SUM(od.Quantity * od.UnitPrice - od.DiscountAmount) AS Revenue
FROM dbo.OrderDetails od
INNER JOIN dbo.Orders o
    ON od.OrderID = o.OrderID
INNER JOIN dbo.Products p
    ON od.ProductID = p.ProductID
WHERE o.OrderStatus = 'Completed'
GROUP BY p.ProductName, p.Category
ORDER BY Revenue DESC;