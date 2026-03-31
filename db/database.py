# db/database.py

import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="circle_db",
        user="taniguchi.airi",
        password="",
        host="localhost"
    )

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()