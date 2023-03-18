# -*- coding: utf-8 -*-
"""
script creates tebles in PostgreSQL database
"""
import psycopg2

conn = psycopg2.connect(database="weather",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

tables_list = ['stacje', 'dane_imgw']

tables = {"stacje": 
                """
                CREATE TABLE stacje (
                    ID serial PRIMARY KEY,
                    nazwa VARCHAR(50) UNIQUE NOT NULL,
                    szer_geo FLOAT,
                    dl_geo FLOAT)
                """,
        "dane_imgw": 
                """
                CREATE TABLE dane_imgw (
                    ID_stacji INTEGER NOT NULL,
                    stacja VARCHAR(50) NOT NULL,
                    data_pomiaru DATE,
                    godzina_pomiaru TIME,
                    temperatura DECIMAL,
                    predkosc_wiatru SMALLINT,
                    kierunek_wiatru SMALLINT,
                    wilgotnosc_wzgledna DECIMAL,
                    suma_opadu DECIMAL,
                    cisnienie DECIMAL,
                    CONSTRAINT fk_stacje
                        FOREIGN KEY (ID_stacji)
                            REFERENCES stacje(ID))
                """
        }


def create_table(conn, table_name):
    cursor = conn.cursor() 
    query_table_exist = "SELECT EXISTS (SELECT * FROM pg_tables WHERE schemaname = 'public' AND tablename = '{}')".format(table_name)
    cursor.execute(query_table_exist)
    flag = cursor.fetchone()[0]
    if flag is True:
        print("tabela {} już istnieje w bazie danych".format(table_name))
    elif flag is False:
        cursor.execute(tables["{}".format(table_name)])
        print("utworzono tabele {}".format(table_name))
    cursor.close()
    conn.commit()


for table_name in tables_list:
    create_table(conn, table_name)

conn.close()

