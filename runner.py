import ConnectivityChecker as cc

hosts = ['192.168.4.48','192.168.4.2']
sockets =['192.168.4.34','192.168.4.48']
cc.check(hosts)
cc.checkSocket(sockets)
