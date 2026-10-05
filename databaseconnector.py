import mysql.connector
from mysql.connector import Error
import pandas as pd
def customer_data(cursor):
    data = pd.read_csv(r"dim_customers.csv")

    for i in data.index:
                # Prepare the SQL INSERT statement
                query = """
                    INSERT INTO customer (customer_key,customer_id,customer_number,first_name,last_name,country,marital_status,gender,birthdate,create_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Extract values from the DataFrame row
                values = tuple(
                    None if pd.isna(value)
                    else value.item() if hasattr(value, "item")
                    else value
                    for value in data.loc[i, [
                        "customer_key", "customer_id", "customer_number",
                        "first_name", "last_name", "country", "marital_status",
                        "gender", "birthdate", "create_date"
                    ]]
                )
                
                # Execute the INSERT statement
                cursor.execute(query, values)
                connection.commit()  # Commit the transaction after each insert


def product_data(cursor):
    data = pd.read_csv(r"dim_products.csv")

    for i in data.index:
                # Prepare the SQL INSERT statement
                query = """
                    INSERT INTO products(product_key,product_id,product_number,product_name,category_id,category,subcategory,maintenance,cost,product_line,start_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                # Extract values from the DataFrame row
                values = tuple(
                    None if pd.isna(value)
                    else value.item() if hasattr(value, "item")
                    else value
                    for value in data.loc[i, [
                        "product_key", "product_id", "product_number",
                        "product_name", "category_id", "category", "subcategory",
                        "maintenance", "cost", "product_line", "start_date"
                    ]]
                )

                # Execute the INSERT statement
                cursor.execute(query, values)
                connection.commit()  # Commit the transaction after each insert

def sales_data(cursor):
    data = pd.read_csv(r"C:\Users\K.SAI RAJA PRANAV\Downloads\sql-data-analytics-project (1)\sql-data-analytics-project\sql-data-analytics-project\datasets\flat-files\fact_sales.csv")

    for i in data.index:
                # Prepare the SQL INSERT statement
        query = """
        INSERT INTO fact_sales(order_number,product_key,customer_key,order_date,shipping_date,due_date,sales_amount,quantity,price)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
                # Extract values from the DataFrame row
        values = tuple(
                None if pd.isna(value)
                else value.item() if hasattr(value, "item")
                else value
                for value in data.loc[i, [
                        "order_number", "product_key", "customer_key",
                        "order_date", "shipping_date", "due_date", "sales_amount", "quantity", "price"
                    ]]
                )

                # Execute the INSERT statement
        cursor.execute(query, values)
        connection.commit()  # Commit the transaction after each insert


def explore_data(cursor):

    q1="select distinct country from customer order by country;"
    q2="select distinct category, subcategory from products order by category;"
    cursor.execute(q1)
    result1 = cursor.fetchall()
    print("Distinct countries in the customer table:")
    data=pd.DataFrame(result1,columns=['country'])
    print(data)
    cursor.execute(q2)
    result2 = cursor.fetchall()
    print("Distinct categories and subcategories in the products table:")
    data2=pd.DataFrame(result2,columns=['category','subcategory'])
    print(data2)

def time_exploration(cursor):
 
            # Add your time exploration queries here
    q1="""SELECT 
    MIN(order_date) AS first_order_date,
    MAX(order_date) AS last_order_date,
    DATEDIFF(MAX(order_date), MIN(order_date)) AS order_range_days
FROM fact_sales;"""
    cursor.execute(q1)
    result1 = cursor.fetchall()
    print("Time exploration results:")
    data=pd.DataFrame(result1,columns=['first_order_date','last_order_date','order_range_months'])
    print(data)
    q2="""SELECT
    MIN(birthdate) AS oldest_birthdate,
    MAX(birthdate) AS youngest_birthdate,
    GETDATE() AS youngest_age
FROM customer;"""
    cursor.execute(q2)
    result2 = cursor.fetchall()
    print("Customer age exploration results:")
    data2=pd.DataFrame(result2,columns=['oldest_birthdate','oldest_age','youngest_birthdate','youngest_age'])
    print(data2)


try:
    # 1. Establish the connection to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",   
        user="root",     # Your MySQL username
        password="password", # Your MySQL password
        database="database_name"  # The database you want to access
    )

    if connection.is_connected():
        print("Successfully connected to the database!")
        cursor = connection.cursor()
        explore_data(cursor)

except Error as e:
        print(f"Error while connecting to MySQL: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed.")