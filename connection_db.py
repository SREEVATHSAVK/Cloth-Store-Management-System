import pymysql

# Establish a connection to the database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='cloth_store'
)

# Create a cursor object to execute SQL queries
mycursor = connection.cursor()