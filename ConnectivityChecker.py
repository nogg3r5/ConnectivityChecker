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
   requests.get(addr,timeout = 5)
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
  type='socket'
  try:
   conn.connect((site, 80))
  except:
   IsUp=False
   writeToDb(site,type,IsUp)
  else:
   IsUp=True
   writeToDb(site,type,IsUp)
 res=[IsUp,site]
 list.append(res)
 print(list)

def writeToDb(site,type,IsUp):
 sqliteConnection = sqlite3.connect('/home/pi/ConnectivityChecker/db/db.sqlite')
 cursor = sqliteConnection.cursor()

 if(IsUp == True):
  lastUp = datetime.now()
  query = f"""select * from ConnectivityCheck where id = '{site}'; """
  cursor.execute(query)
  data = cursor.fetchall()
  lastDown=data[0][4]
  cursor.execute("INSERT or replace INTO ConnectivityCheck (id,type,lastUp,lastDown,IsUp) values(?, ?, ?, ?,?)",(site,type,lastUp,lastDown,IsUp))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()

 else:
  query = f"""select * from ConnectivityCheck where id = '{site}'; """
  cursor.execute(query)
  data = cursor.fetchall()
  lastUp=data[0][3]
  lastDown = datetime.now()
  cursor.execute("INSERT or replace INTO ConnectivityCheck (id,type,lastUp,lastDown,IsUp) values(?, ?, ?, ?, ?)",(site,type,lastUp,lastDown,IsUp))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()

#CREATE TABLE ConnectivityCheck (id text primary key autoincrement,type TEXT,lastcheck DATETIME default current_timestamp,lastUp datetime,lastDown datetime,IsUp integer);


if __name__ == "__main__":
    check(args)
