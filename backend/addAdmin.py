"""
This script is used to add an admin user to the database. 
It connects to the database using the credentials provided in the dbinfo module and
creates a new admin user with the specified username and password.
"""
import pymysql
import dbinfo
import bcrypt

connection = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"], 
user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"], database=dbinfo.data["DBNIMI"])
cursor = connection.cursor()

def add_admin(username, password):
    """
    Add a new admin to the database.
    """
    cursor.execute("INSERT INTO admin (username, pword) VALUES (%s, %s)", (username, password))
    connection.commit()
    print(f"Admin '{username}' added successfully.")

if __name__ == "__main__":
    new_admin_username = input("Enter the new admin's username: ")
    new_admin_password = input("Enter the new admin's password: ")
    hashed_password = bcrypt.hashpw(new_admin_password.encode('utf-8'), bcrypt.gensalt())
    add_admin(new_admin_username, hashed_password)
