import requests
import sys
import socket
import sqlite3

#to be replaced with argparse
#args = sys.argv[1:]

def checkArgs():
 if not args:
  sys.exit('please pass at least one url as an argument')

def check(sites):
 #checkArgs()
 list = []
 for site in sites:
  site = 'http://' + site
  res = [requests.get(site),site]
  list.append(res)
 print(list)

def checkSocket(sites):
 for site in sites:
  conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
   conn.connect((site, 80))
   res='success'
   print(res+' '+site)
  except:
   res='failure'
   print(res+' '+site)
   return
#First imte i've used this, runs the script only if being called from cli. __name__ only == __main__ when run from cli
#When imorted, main is still available, but will not be executed.
if __name__ == "__main__":
    check(args)
