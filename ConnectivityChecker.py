import requests
import json

def main(sites):
 list = []
 foreach $site in $sites:
  res = requests.get($site)
  list.append(res)
 return list
