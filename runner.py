import ConnectivityChecker as cc

hosts = ['192.168.4.48','nogg3r5.hopto.org']
sockets =['192.168.4.34']

print('Conventional hosts...')
cc.check(hosts)
print('')
print('Sockets...')
cc.checkSocket(sockets)
