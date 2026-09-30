# AI Business Analyst Assistant

An AI-powered business analytics dashboard for a clothing retail business. The application connects to a SQL Server database, analyzes sales and inventory data, visualizes key performance indicators, and answers business questions through a chat interface.

## Project Overview

This project demonstrates how SQL, Python, Streamlit, and generative AI can work together to support business decision-making.

It is designed around a sample clothing retail dataset containing products, customers, orders, order details, inventory transactions, and sales targets.

## Features

### Sales Analytics
- Total revenue
- Gross profit and product cost
- Completed order count
- Total units sold
- Average order value
- Monthly revenue analysis
- Revenue by product category
- Top-selling products

### Inventory Analytics
- Remaining stock by product
- Inventory transaction tracking
- Low-stock alerts
- Total remaining inventory

### Interactive Dashboard
- KPI cards
- Monthly revenue chart
- Category revenue chart
- Top-selling products chart
- Remaining inventory chart
- Automatically generated business insights

### AI Business Assistant
Ask business questions such as:
- What is our total revenue?
- What is our gross profit?
- Which month had the highest revenue?
- Which product sold the most units?
- Which products are low in stock?
- How much inventory stock is remaining?

The application uses SQL-based business calculations and can use Gemini to generate conversational responses when API access is available.

## Technology Stack

- Python
- SQL Server Express
- SQL
- Streamlit
- Pandas
- Altair
- Google Gemini API
- VS Code

## Database

Database name: `AIBusinessAnalystDB`

Main tables:
- `Customers`
- `Products`
- `Orders`
- `OrderDetails`
- `InventoryTransactions`
- `SalesTargets`

## Sample Business Results

The sample dataset currently produces these results:

| Metric | Result |
|---|---:|
| Total Revenue | ₹48,700 |
| Total Product Cost | ₹24,100 |
| Gross Profit | ₹24,600 |
| Completed Orders | 9 |
| Units Sold | 32 |
| Remaining Inventory | 553 pieces |
| Highest Revenue Month | February 2025 |
| Top-Selling Product | Classic T-Shirt |
| Low-Stock Product | Leather Handbag |

These are results from the included sample dataset, not live business performance figures.

## Project Structure

```text
AI Business Analyst Assistant/
│
├── app.py
├── app_backup.py
├── business_data.py
├── analytics.py
├── visualize.py
├── test_connection.py
├── test_analytics.py
├── inspect_database.py
│
├── 01_Create_And_Select_Database.sql
├── 02_Create_Tables.sql
├── 03_Insert_Sample_Business_Data.sql
├── 04_Verify_Table_Record_Counts.sql
├── 05_View_Table_Column_Structure.sql
│
├── .gitignore
└── README.md