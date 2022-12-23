import requests
import sys
import socket
import sqlite3

def check(sites):
 list = []
 for site in sites:
  addr = 'http://' + site
  try:
   requests.get(addr)
   req=True
   writeToDb(True)
  except:
   req=False
   writeToDb(False)
  res = [req,site]
  list.append(res)
 print(list)

def checkSocket(sites):
 list=[]
 for site in sites:
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
   conn.connect((site, 80))
   req=True
   writeToDb(True)
  except:
   req=False
   writeToDb(False)
 res=[req,site]
 list.append(res)
 print(list)

def writeToDb(isup):
 #sqliteConnection = sqlite3.connect('/home/pi/ConnectivityChecker/db/db.sqlite')
 #cursor = sqliteConnection.cursor()

 if(isup == True):
  #lastUp=date
  print("Is up would be written todb")
 else:
  print("Is down would be wrtten to DB")
  #lastdown=date
  #lastUp=get from db

 #cursor.execute("INSERT INTO ConnectivityCheck (site,type,lastUp,lastDown,IsUp) values(?, ?, ?, ?, ?)",(site,type,lastUp,lastDown,IsUp))
 #sqliteConnection.commit()
 #cursor.close()
 #sqliteConnection.close()


#CREATE TABLE ConnectivityCheck (id integer primary key autoincrement,site TEXT,type TEXT,lastcheck DATETIME default current_timestamplastUp datetime,lastDown datetime,IsUp integer);


if __name__ == "__main__":
    check(args)
