# Python program to implement server side of chat room.
import socket
import select
import sys
from thread import *
 
"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number
Port = int(sys.argv[2])
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
 
list_of_clients = []
 
def clientthread(conn, addr):
 
    # sends a message to the client whose user object is conn
    conn.send("Welcome to this chatroom!")
 
    while True:
            try:
                message = conn.recv(2048)
                PorB = message[:5]
                
                if message:
 
                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    #print len(list_of_clients)
                    if(PorB == "broad"):
                        message = message[10:]
                        print "<" + addr[0] + "> " + message
 						
                    # Calls broadcast function to send message to all
                        message_to_send = "<" + addr[0] + "> " + message
                        broadcast(message_to_send, conn)
                   	
                    
                    elif(PorB == "messa"):
                        recipient = message[8:]
                        i=0
                        while(recipient[i]!=' '):
                            i=i+1
 						
                        message = recipient[i+1:]
                        recipient = recipient[:i]
                        message_to_send = "<" + addr[0] + "> " + message
                        p2p(message_to_send, conn, recipient)
 					
                    elif(PorB == "whoel"):
                        whoel(list_of_clients,conn)
                            	
                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)
 
            except:
                continue
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def whoel(online_users, connection):
    for clients in list_of_clients:
        if clients[0]!=connection:
            print clients[1]

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients[0]!=connection:
            try:
                clients[0].send(message)
            except:
                clients[0].close()
 
                # if the link is broken, we remove the client
                remove(clients[0])

def p2p(message, connection, recipient):
    rec_online=1
    for clients in list_of_clients:
        if clients[0]!=connection:
            if(clients[1]==recipient):
                try:
                    clients[0].send(message)
                except:
                    clients[0].close()
            else:
                print "save message here"
 
                # if the link is broken, we remove the client
                remove(clients)
  
"""The following function simply removes the object
from the list that was created at the beginning of 
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 
while True:
 
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append((conn,addr[0]))

 
    # prints the address of the user that just connected
    print addr[0] + " connected"
 
    # creates and individual thread for every user 
    # that connects
    start_new_thread(clientthread,(conn,addr))    
 
conn.close()
server.close()
