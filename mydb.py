# Install mysql onto the computer
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python (only if the one above doesn't work)

import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'dhawan'
)

# prepare cursor object
cursorObject = db.cursor()

# Create database
cursorObject.execute("CREATE DATABASE websitedb")

print("database created")