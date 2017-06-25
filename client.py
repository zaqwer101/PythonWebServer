import socket

import time

i = 0
while True:
    time.sleep(1)
    sock = socket.socket()
    sock.connect(("127.1", 3228))
    print( sock.recv(16384).decode() )
    i = i + 1
    sock.close()
