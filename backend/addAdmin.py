"""Create an administrator account with a bcrypt password hash."""

import getpass

import bcrypt
import pymysql

import dbinfo


def main():
    username = input("Enter the new admin's username: ").strip()
    password = getpass.getpass("Enter the new admin's password: ")

    if not username or len(username) > 45:
        raise ValueError("Username must contain 1 to 45 characters.")
    if not 12 <= len(password.encode("utf-8")) <= 72:
        raise ValueError("Admin passwords must be between 12 and 72 bytes.")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    connection = pymysql.connect(
        host=dbinfo.data["HOST"],
        port=dbinfo.data["PORT"],
        user=dbinfo.data["USER"],
        password=dbinfo.data["PASSWORD"],
        database=dbinfo.data["DBNIMI"],
        charset="utf8mb4",
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO admin (username, pword) VALUES (%s, %s)",
                (username, password_hash.decode("ascii")),
            )
        connection.commit()
    finally:
        connection.close()
    print(f"Admin '{username}' added successfully.")


if __name__ == "__main__":
    main()
