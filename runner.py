import ConnectivityChecker as cc

hosts =['pizero2.tail06b125.ts.net:5000','raspberrypi4b.tail06b125.ts.net:3000/dashboard','google.co.uk']
sockets =['192.168.4.34']
services =['PersonalDashboard']

print('Conventional hosts...')
cc.check(hosts)
print('')
print('Sockets...')
cc.checkSocket(sockets)
print('Services...')
cc.checkServices(services)
