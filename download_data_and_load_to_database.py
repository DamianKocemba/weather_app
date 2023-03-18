# -*- coding: utf-8 -*-
"""
download data using IMGW API
and load data to database table
"""
import requests
import json
import psycopg2


conn = psycopg2.connect(database="weather",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432")

def get_imgw_data():
    url = 'https://danepubliczne.imgw.pl/api/data/synop'
    response = requests.get(url)
    response = json.loads(response.text)
    #convert hours to time format
    for stacja in response:
        stacja['godzina_pomiaru'] = stacja['godzina_pomiaru'] + ":00"
    return json.dumps(response) #convert to string


data = get_imgw_data()

cursor = conn.cursor()
query_insert_imgw_data = """
                        INSERT INTO dane_imgw SELECT * FROM 
                        json_populate_recordset(NULL::dane_imgw, %s)
                        """

cursor.execute(query_insert_imgw_data, (data,))
conn.commit()
conn.close()