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
  if len(data) > 0:
   lastDown=data[0][4]
  downCount = 0
  cursor.execute("INSERT or replace INTO ConnectivityCheck (id,type,lastUp,lastDown,IsUp,count) values(?, ?, ?, ?, ?, ?)",(site,type,lastUp,lastDown,IsUp,downCount))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()

 else:
  lastDown = datetime.now()
  query = f"""select * from ConnectivityCheck where id = '{site}'; """
  cursor.execute(query)
  data = cursor.fetchall()
  if len(data) > 0:
   lastUp=data[0][3]
   downCount=data[0][6]
  else:
   downCount=0
   lastUp=0
  downCount=int(downCount)
  if downCount == 0:
   downCount = 1
  else:
   downCount = downCount+1
  cursor.execute("INSERT or replace INTO ConnectivityCheck (id,type,lastUp,lastDown,IsUp,count) values(?, ?, ?, ?, ?, ?)",(site,type,lastUp,lastDown,IsUp,downCount))
  sqliteConnection.commit()
  cursor.close()
  sqliteConnection.close()
  if downCount > 5:
   requests.get('https://api.pushcut.io/trJMTZmRdcjHkiGiWnt4Z/notifications/ConnectivityCheck%20Failed')


#CREATE TABLE ConnectivityCheck (id text primary key autoincrement,type TEXT,lastcheck DATETIME default current_timestamp,lastUp datetime,lastDown datetime,IsUp integer);


if __name__ == "__main__":
    check(args)
