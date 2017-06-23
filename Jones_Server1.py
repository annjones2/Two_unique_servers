# Jones_Server1.py
# provides client with chat room

#imports
from socket import *
import sys
from sys import argv
import select
import time

if(len(argv) < 2) :
        print 'Usage : python Jones_Server1.py <first port number>'
        sys.exit()
#local ip address
host = '' 
#port number 1 from user
port = int(argv[1])
#address
address = (host, port)
#variables
socket_list = []
recv_buffer = 4096 

def chat_server():
	#socket to connect to multiple clients
    serv_sock = socket(AF_INET, SOCK_STREAM)
    #reusable
    serv_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serv_sock.bind(address)
	#up to 10 clients can chat
    serv_sock.listen(10)
 
    # add server socket object to added connections
    socket_list.append(serv_sock)
 
    print "Chat server started on port " + str(port)
 
    while 1:
        # socket_list adds new clients and 0 is for timeout
        ready_to_read, ready_to_write, in_error = select.select(socket_list,[],[],0)
      
        for sock in ready_to_read:
            # when new client connects with server
            if sock == serv_sock: 
                sockfd, addr = serv_sock.accept()
                socket_list.append(sockfd)
                print "Client (%s, %s) is connected" % addr
                broadcast(serv_sock, sockfd, "[%s:%s] entered your chat room\n" % addr)
            # client message
            else:
                try:
                    # receiving data
                    data = sock.recv(recv_buffer)
                    if data:
                        # there is something in the socket
                        broadcast(serv_sock, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        #broken socket   
                        if sock in socket_list:
                            socket_list.remove(sock)
						#inform other clients
                        broadcast(serv_sock, sock, "Client [%s, %s] went offline\n" % addr)
                except:
                    broadcast(serv_sock, sock, "Client [%s, %s] went offline\n" % addr)
                    continue

    serv_sock.close()
    
# define broadcast
def broadcast (serv_sock, sock, message):
    for socket in socket_list:
        # send the message only to peer
        if socket != serv_sock and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in socket_list:
                    socket_list.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())        

