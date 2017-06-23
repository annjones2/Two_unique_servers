# Jones_client.py
# client connects to Jones_Server1.py and Jones_Server2.py

#imports
import sys
from sys import argv
import socket
import select



# socket for Jones_Server2
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# from user
host1 = argv[3]
port1 = int(argv[4])
# connect
try :
	s1.connect((host1, port1))
except :
	print 'Unable to connect with Jones_Server2'
	sys.exit()
# Receive time in variable time
time = s1.recv(1024)                                     

s1.close()

#end for Jones_Server2
#start for Jones_Server1
def chat_client():
    if(len(argv) < 4) :
        print 'Usage:  python Jones_Client.py <first ip address> <first port number> <second ip address> <second port number>'
        sys.exit()

    host = argv[1]
    port = int(argv[2])
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect with Jones_Server1'
        sys.exit()
     
    print 'You connected at time %sYou can begin writing messages' % time.decode('ascii')
    sys.stdout.write('Client: '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:            
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('Client: '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('Client: '); sys.stdout.flush() 

if __name__ == "__main__":

    sys.exit(chat_client())


