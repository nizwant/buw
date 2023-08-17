import sqlite3
from datetime import datetime
from buw import get_buw


def create_tables(con: sqlite3.Connection):
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE day (
        day_id INTEGER PRIMARY KEY,
        pretty_date TEXT,
        date TEXT,
        opening_hour TEXT,
        closing_hour TEXT
        )"""
    )
    cur.execute(
        """CREATE TABLE weather (
        weather_id INTEGER PRIMARY KEY,
        temp_c REAL,
        feelslike_c REAL,
        precip_mm REAL,
        cloud int,
        humidity int,
        pressure_mb REAL,
        condition text,
        last_updated text
        )"""
    )
    cur.execute(
        """CREATE TABLE people_quantity (
        minute_id INTEGER PRIMARY KEY,
        weather_id INTEGER,
        day_id INTEGER,
        quantity int,
        time text)
        """
    )
    _, _, date, opening_hour, closing_hour = get_buw()
    cur.execute(
        """INSERT INTO day (pretty_date, date, opening_hour, closing_hour) VALUES (?, ?, ?, ?)""",
        (date, datetime.now().strftime("%Y-%m-%d"), opening_hour, closing_hour),
    )
