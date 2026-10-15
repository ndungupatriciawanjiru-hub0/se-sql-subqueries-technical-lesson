# SQL Subqueries - model toy company (CRM database)
import sqlite3
import pandas as pd

# Connect to the SQLite database (data.sqlite must be in the same folder)
conn = sqlite3.connect('data.sqlite')

# --- Task 1: Employees from the United States ---
# Subquery returns the US office codes; outer query filters employees by them
q1 = """
SELECT lastName, firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    WHERE country = "USA"
)
;"""
print("Employees from the USA")
print(pd.read_sql(q1, conn), "\n")

# --- Task 2: Employees from offices with at least 5 employees ---
# Subquery groups employees by office and keeps offices with 5+ people
q2 = """
SELECT lastName, firstName, officeCode
FROM employees
WHERE officeCode IN (
    SELECT officeCode
    FROM offices
    JOIN employees USING(officeCode)
    GROUP BY officeCode                    -- one row per office
    HAVING COUNT(employeeNumber) >= 5      -- filter on the aggregate
)
;"""
print("Employees from offices with 5+ employees")
print(pd.read_sql(q2, conn), "\n")

# --- Task 3: Chained aggregates (average of customers' average payments) ---
# Inner query: average payment per customer; outer query: average of those
q3 = """
SELECT AVG(customerAvgPayment) AS averagePayment
FROM (
    SELECT AVG(amount) AS customerAvgPayment
    FROM payments
    JOIN customers USING(customerNumber)
    GROUP BY customerNumber
)
;"""
print("Average of customer average payments")
print(pd.read_sql(q3, conn), "\n")

# --- Task 4: Match employeeNumber to salesRepEmployeeNumber ---
# Keys have different names; this returns reps serving US customers
q4 = """
SELECT lastName, firstName, employeeNumber
FROM employees
WHERE employeeNumber IN (
    SELECT salesRepEmployeeNumber
    FROM customers
    WHERE country = "USA"
)
;"""
print("Sales reps with customers in the USA")
print(pd.read_sql(q4, conn), "\n")

# Always close the connection when done
conn.close()