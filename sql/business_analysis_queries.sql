/*
Created database in SQL Shell(psql) with command
Create database DA_projects
*/

CREATE TABLE superstore (
    row_id INT,
    order_id VARCHAR(50),
    order_date DATE,
    ship_date DATE,
    ship_mode VARCHAR(50),
    customer_id VARCHAR(50),
    customer_name VARCHAR(150),
    segment VARCHAR(50),
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    region VARCHAR(50),
    product_id VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    product_name TEXT,
    sales NUMERIC(10,4),
    quantity INT,
    discount NUMERIC(5,2),
    profit NUMERIC(10,4)
);
/*
 imported data using SQL Shell(psql) with the command
 \copy superstore FROM 'C:/Users/user/DA1project/data/cleaned_superstore.csv' DELIMITER ',' CSV HEADER;
 
 (COPY → PostgreSQL server reads file → permission issue
  \copy → your local machine reads file → works safely)
 */

SELECT COUNT(*) FROM superstore;

SELECT * FROM superstore
LIMIT 5;

/* Business Analysis Queries */

-- Query-1
-- Finding Top 10 Profitable customers (Which customers create most profit?)
-- Top 10 customers contribute large portion of profit.
SELECT customer_name,
SUM(profit) AS total_profit
FROM superstore
GROUP BY customer_name
ORDER BY total_profit DESC
LIMIT 10;

-- Query-2
-- Monthly Revenue trend (How sales behave over time?)
-- Revenue spikes during year-end months.
SELECT DATE_TRUNC('month', order_date) AS month,
SUM(sales) AS total_sales
FROM superstore
GROUP BY month
ORDER BY month;

-- Query-3
-- Loss-Making Top 10 Products(Which products hurt business?)
-- High discount lowers average profit.
SELECT product_name,
SUM(profit) AS total_profit
FROM superstore
GROUP BY product_name
HAVING SUM(profit) < 0
ORDER BY total_profit
Limit 10;

---- Query-4
-- Analysig Discount Impact
/*
This gives direct business insight:
discount vs profitability
higher discount reduces profit 
*/
SELECT discount,
AVG(profit) AS avg_profit
FROM superstore
GROUP BY discount
ORDER BY discount;

-- Query-5
-- Region-Wise Sales Ranking (Top customers inside each region) 
-- using Window function
SELECT region,
customer_name,
SUM(sales) AS total_sales,
RANK() OVER (
PARTITION BY region
ORDER BY SUM(sales) DESC
) AS rank
FROM superstore
GROUP BY region, customer_name;

-- Query-6
-- Top Performing Category
SELECT category,
SUM(sales) AS total_sales,
SUM(profit) AS total_profit
FROM superstore
GROUP BY category
ORDER BY total_profit DESC;

--Query-7
-- Repeat Purchase Frequency by Customer
/* 
customers with highest number of orders
repeated customers
loyal customer base
*/

SELECT customer_name,
COUNT(order_id) AS total_orders
FROM superstore
GROUP BY customer_name
HAVING COUNT(order_id) > 1
ORDER BY total_orders DESC;

-- Query-8
-- Repeated customers + total profit 
SELECT customer_name,
COUNT(order_id) AS total_orders,
SUM(profit) AS total_profit
FROM superstore
GROUP BY customer_name
HAVING COUNT(order_id) > 1
ORDER BY total_orders DESC;

--Query-9
-- Top 10 loyal customers
SELECT customer_name,
COUNT(order_id) AS total_orders,
SUM(sales) AS total_sales,
SUM(profit) AS total_profit
FROM superstore
GROUP BY customer_name
ORDER BY total_orders DESC
LIMIT 10;

/*
Insight
- Top repeat customers contribute significantly to revenue
- Some frequent buyers generate low profit
- Loyalty does not always mean profitability
*/

DROP TABLE IF EXISTS superstore;