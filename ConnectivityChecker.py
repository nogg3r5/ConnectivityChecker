import requests
import sys
import socket
import sqlite3
from datetime import datetime
import os
import subprocess

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='ConnectivityChecker.log', encoding='utf-8', level=logging.INFO,format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s')
#logger.debug('This message should go to the log file')
logger.info('Connectivity Checker Ran')
#logger.warning('And this, too')
#logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

def checkServices(services):
 logger.info('Connectivity Checker checked Services')
 list=[]
 for service in services:
  type='service'
  status = os.system('systemctl is-active --quiet '+ service)
 if status == 0:
  IsUp = True
  writeToDb(service,type,IsUp)
 else:
  IsUp = False
  writeToDb(service,type,IsUp)
 res = [IsUp,service]
 list.append(res)
 print(list)

def check(sites):
 logger.info('Connectivity Checker checked Sites')
 list = []
 for site in sites:
  addr = 'http://' + site
  type='site'
  try:
   requests.get(addr,timeout = 5)
  except Exception as e:
   IsUp=False
   writeToDb(site,type,IsUp)
   logger.warning('Connectivity Checker restarted Tailscale')
   subprocess.run(["/usr/bin/tailscale","down","--accept-risk=lose-ssh"]) 
   subprocess.run(["/usr/bin/tailscale","up"])
  else:
   IsUp=True
   writeToDb(site,type,IsUp)

  res = [IsUp,site]
  list.append(res)
 print(list)

def checkSocket(sites):
 logger.info('Connectivity Checker checked Sockets')
 list=[]
 for site in sites:
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  conn.settimeout(10.0)
  type='socket'
  try:
   conn.connect((site, 80))
  except Exception as e:
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
  else:
   lastDown = 'null'
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
