# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
geocoding IMGW stations (get coordinates of cities/places)
it's not accurate coordinates of stations
"""
from geopy.geocoders import Nominatim
import psycopg2

path = "C://Users//damia//OneDrive//Pulpit//Python//api//"
file = "stacje.csv"

#get list of stations from csv file
stacje_dict = {}
with open(path+file, encoding='utf8') as stacje_meteo:
    for stacja in stacje_meteo:
        idx = stacja.split(",")[0]
        stacja = stacja.split(",")[1]
        stacje_dict[idx] = stacja


conn = psycopg2.connect(database="weather",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

nom = Nominatim(user_agent="http") #choice of OpenStreetMap geocoding web service

#geocode cities - get geographical coordinates
def geocoding_to_table(connection, id_stacji, nazwa_stacji):
    cursor = connection.cursor()
    query_insert_data = "INSERT INTO stacje (ID, nazwa, szer_geo, dl_geo) VALUES (%s, %s, %s, %s)"
    try:
        n = nom.geocode(nazwa_stacji + ", Polska")
        cursor.execute(query_insert_data, (id_stacji, nazwa_stacji,  n.latitude, n.longitude))
        print(stacja, n.latitude, n.longitude)
    except:
        cursor.execute(query_insert_data, (indeks, stacja, None, None))
        print(stacja, None, None)
    connection.commit()


for indeks, stacja in stacje_dict.items():
    geocoding_to_table(conn, indeks, stacja)

conn.close()


