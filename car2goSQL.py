from urllib2 import urlopen
from bs4 import BeautifulSoup
import re, time
#import pymysql.cursors

#Webpage connection
html = urlopen('http://cardivvy.com/cars.php?location=Vancouver&lat=49.2625&lon=-123.114')
        
#scripe the website with BS
bsObj2 = BeautifulSoup(html,"html.parser")
        
#store the time (UTC)
ts = time.time()
        
#extract location and car info
location = bsObj2.findAll("div", {"class" : "col-md-4",})
carinfo = bsObj2.findAll("div", {"class" : "col-md-8",})
        
#extract exact info
car_list = []
        
for (item,loc) in zip(carinfo,location):
    item2 = str(item)
    loc2 = str(loc)
    loc3 = loc2.split('=')[3]
    car = {'lic':item2.split(' ')[2],'eng':item2.split(' ')[5],'fuel':item2.split(' ')[8],
    'exte':item2.split(' ')[11],'inte':item2.split(' ')[14].split('<')[0],
    'lat':loc3.split(',')[0],'lon':loc3.split(',')[1].split('"')[0], 'time':ts}
    car_list.append(car)
        
            
#store
#connect to SQL
import sqlite3
        
#make a database to store the data if one doesnt exist
DATABASE = 'C:\CS\Car2go\output\car2go.sqlite'
conn = sqlite3.connect(DATABASE)
c = conn.cursor()
        
#create a table if not exists
sql = '''CREATE TABLE IF NOT EXISTS vancouver
        (id INTEGER PRIMARY KEY, lic TEXT, eng TEXT, fuel REAL, exte TEXT,
       inte TEXT, lat REAL, lon REAL, time REAL)'''
c.execute(sql)
        
#add data
for i in car_list:
     c.execute("INSERT INTO vancouver VALUES (null, :lic, :eng, :fuel, :exte, :inte, :lat, :lon, :time)", i)
     conn.commit()
