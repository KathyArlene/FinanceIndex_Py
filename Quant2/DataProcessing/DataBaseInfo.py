import pymysql

# Connect to the database
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="Zyyjjdl6543201",
    database="sp500_history"
)

# Create a cursor object
cursor = connection.cursor()

# Execute a SQL query to get all tables in the database
cursor.execute("SHOW TABLES")

# Fetch all tables from the cursor
tables = cursor.fetchall()

# Iterate over the tables and print their information
for table in tables:
    table_name = table[0]
    print("Table Name: {}".format(table_name))

    # Execute a SQL query to get all columns in the table
    cursor.execute("DESCRIBE {}".format(table_name))

    # Fetch all columns from the cursor
    columns = cursor.fetchall()

    # Print column names and types
    for column in columns:
        column_name = column[0]
        column_type = column[1]
        print("\t{} ({})".format(column_name, column_type))

    print("\n") # Add a new line between tables

# Close the cursor and connection
cursor.close()
connection.close()
