import sqlite3
import os
from datetime import datetime
from create_db import create_tables
from buw import get_buw
from warsaw_weather import get_current_weather


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    path_to_db = os.path.join(path, "buw.db")

    # check if database exists
    # if not create it
    if not os.path.isfile(path_to_db):
        con = sqlite3.connect(path_to_db)
        create_tables(con)
        con.commit()
        con.close()

    # get data about occupancy and weather
    number_of_people, time, date, opening_hour, closing_hour = get_buw()
    (
        temp_c,
        feelslike_c,
        precip_mm,
        cloud,
        humidity,
        pressure_mb,
        condition,
        last_updated,
    ) = get_current_weather()
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()

    # insert into day table
    if datetime.now().hour == 0 and datetime.now().minute == 1:
        cur.execute(
            """INSERT INTO day (pretty_date, date, opening_hour, closing_hour) VALUES (?, ?, ?, ?)""",
            (date, datetime.now().strftime("%Y-%m-%d"), opening_hour, closing_hour),
        )
        con.commit()

    # insert into weather table
    cur.execute(
        """SELECT last_updated FROM weather
                ORDER BY weather_id DESC
                LIMIT 1"""
    )
    last_weather = cur.fetchone()
    if last_weather is None or last_weather[0] != last_updated:
        cur.execute(
            """INSERT INTO weather (temp_c, feelslike_c, precip_mm, cloud, humidity, pressure_mb, condition, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                temp_c,
                feelslike_c,
                precip_mm,
                cloud,
                humidity,
                pressure_mb,
                condition,
                last_updated,
            ),
        )
        con.commit()

    # insert into people_quantity table
    cur.execute("""SELECT day_id FROM day ORDER BY day_id DESC LIMIT 1""")
    day_id = cur.fetchone()[0]
    cur.execute("""SELECT weather_id FROM weather ORDER BY weather_id DESC LIMIT 1""")
    weather_id = cur.fetchone()[0]
    cur.execute(
        """INSERT INTO people_quantity (day_id, weather_id, quantity, time) VALUES (?, ?, ?, ?)""",
        (day_id, weather_id, number_of_people, time),
    )
    con.commit()

    # to remove
    cur.execute("""SELECT * FROM people_quantity""")
    print(cur.fetchall())
    cur.execute("""SELECT * FROM weather""")
    print(cur.fetchall())
    cur.execute("""SELECT * FROM day""")
    print(cur.fetchall())
    con.close()


if __name__ == "__main__":
    main()
