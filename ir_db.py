import os

import mysql.connector
from mysql.connector import Error


DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "incident_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
    )


def test_connection():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM incident_reports LIMIT 1")
            cursor.fetchone()
            return True, "Koneksyon sa Incident Report database ay maayos na."
        return False, "Hindi makakonekta sa database."
    except Error as error:
        return False, str(error)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def next_ir():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT ir_no FROM incident_reports ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        if not result:
            return "IR-0001"
        last_no = result[0]
        try:
            num = int(last_no.split("-")[1]) + 1
            return f"IR-{num:04d}"
        except (IndexError, ValueError):
            return "IR-0001"
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def save_report(record):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO incident_reports
                (ir_no, reported_by, incident_date, incident_time, location, incident_type,
                 persons_involved, narrative, action_taken, reported_to, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                record["ir_no"],
                record["reported_by"],
                record["incident_date"],
                record["incident_time"],
                record["location"],
                record["incident_type"],
                record["persons_involved"],
                record["narrative"],
                record["action_taken"],
                record["reported_to"],
                record["status"],
            ),
        )
        connection.commit()
        return cursor.lastrowid
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def all_reports():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM incident_reports ORDER BY incident_date DESC, incident_time DESC")
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_report(ir_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM incident_reports WHERE ir_no = %s", (ir_no,))
        return cursor.fetchone()
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_status(ir_no, action_taken, reported_to, status):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE incident_reports
            SET action_taken = %s, reported_to = %s, status = %s
            WHERE ir_no = %s
            """,
            (action_taken, reported_to, status, ir_no),
        )
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_report(ir_no):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM incident_reports WHERE ir_no = %s", (ir_no,))
        connection.commit()
        return cursor.rowcount > 0
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_all():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connectioncursor.execute("DELETE FROM incident_reports")
        connection.commit()
        return cursor.rowcount
    except Error:
        if connection is not None:
            connection.rollback()
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

