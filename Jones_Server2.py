# Jones_Server2.py
# Current Time server

#imports
from socket import *
import sys
from sys import argv
import select
import time

# create a socket object
serversocket = socket(AF_INET, SOCK_STREAM) 
# local ip address
host = ''                           
# port number from user
port = int(argv[1])
# bind
serversocket.bind((host, port))                                  
#listen
serversocket.listen(10)                                           

while True:
    clientsocket,addr = serversocket.accept()      

    print("Got a connection from %s" % str(addr))
    currentTime = time.ctime(time.time()) + "\r\n"
    clientsocket.send(currentTime.encode('ascii'))
    clientsocket.close()
