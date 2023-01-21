import requests
import sys
import socket
import sqlite3
from datetime import datetime

def check(sites):
 list = []
 for site in sites:
  addr = 'http://' + site
  type='site'
  try:
   print(addr)
   requests.get(addr)
  except:
   IsUp=False
   writeToDb(site,type,IsUp)
  else:
   IsUp=True
   writeToDb(site,type,IsUp)

  res = [IsUp,site]
  list.append(res)
 print(list)

def checkSocket(sites):
 list=[]
 for site in sites:
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
   conn.connect((site, 80))
   req=True
   writeToDb(site,type,IsUp)
  except:
   req=False
   writeToDb(False)
 res=[req,site]
 list.append(res)
 print(list)

def writeToDb(site,type,IsUp):
 sqliteConnection = sqlite3.connect('/home/pi/ConnectivityChecker/db/db.sqlite')
 cursor = sqliteConnection.cursor()

 if(IsUp == True):
  lastUp = datetime.now()
  print("Is up would be written todb")
  print(site,type,lastUp,IsUp)
  cursor.execute("INSERT or replace INTO ConnectivityCheck (site,type,lastUp,IsUp) values(?, ?, ?, ?)",(site,type,lastUp,IsUp))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()

 else:
  print("Is down would be wrtten to DB")
  #lastdown=date
  #lastUp=get from db



#CREATE TABLE ConnectivityCheck (id integer primary key autoincrement,site TEXT,type TEXT,lastcheck DATETIME default current_timestamp,lastUp datetime,lastDown datetime,IsUp integer);


if __name__ == "__main__":
    check(args)
