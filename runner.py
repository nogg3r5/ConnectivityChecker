import ConnectivityChecker as cc

hosts =['192.168.4.48','raspberrypi4b.tail06b125.ts.net:3000/dashboard']
sockets =['192.168.4.34']
services =['PersonalDashboard']

print('Conventional hosts...')
cc.check(hosts)
print('')
print('Sockets...')
cc.checkSocket(sockets)
print('Services...')
cc.checkServices(services)
