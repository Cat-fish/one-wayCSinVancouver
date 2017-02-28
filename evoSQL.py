#from urllib2 import urlopen
#from bs4 import BeautifulSoup
import re, time
import json, requests
import sqlite3
#import pymysql.cursors

#access the url and copy data
url = 'https://evo.ca/api/Cars.aspx'
resp = requests.get(url=url)
data = json.loads(resp.text)

#store the time (UTC)
ts = time.time()

#store data
data2 = data['data'] #this part contains the actual data (list of dict)
car_list = []
for i in xrange(0,len(data2)):
    car = {'plate':data2[i]['Plate'],'name':data2[i]['Name'], 'lon':data2[i]['Lon'], 'fuel':data2[i]['Fuel'],
           'add':data2[i]['Address'], 'lat':data2[i]['Lat'], 'id':data2[i]['Id'], 'time':ts}
    #print data2[i]['Name']
    car_list.append(car)

#store the data into SQLdb
#make a database to store the data if one doesnt exist
DATABASE = 'C:\CS\Evo\output\evo.sqlite'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()



#create a table if not exists
sql= '''CREATE TABLE IF NOT EXISTS vancouver
        (id INTEGER PRIMARY KEY, lic TEXT, fuel REAL, lat REAL, lon REAL, time REAL, name TEXT, address TEXT, hash TEXT)'''
c.execute(sql)

#add data
for i in car_list:
    c.execute('INSERT INTO vancouver VALUES (null, :plate, :fuel, :lat, :lon, :time, :name, :add, :id)',i)
    conn.commit()




