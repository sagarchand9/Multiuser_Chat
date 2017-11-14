# Python program to implement client side of chat room.
import socket
import select
import sys
 
server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 4:
    print "Correct usage: script, IP address, port number, username:password"
    exit()

userpass = str(sys.argv[3])
#passname = str(sys.argv[4])   

if not len(userpass.split(":",1)) == 2:
    print "wrong format for user name and password"
    exit(0)

IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server1.connect((IP_address, Port))
server1.send(userpass)



#print server1

#i = 1
while True:
 
    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server1]
 
    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
 
    for socks in read_sockets:
        #print str(socks) + " " + str(i)
        if socks == server1:
            message = socks.recv(2048)
            #print "message length" + str(len(message))
            if len(message) == 0:
                print "Connection closed\n"
                server1.close()
                exit(0)
            elif message == "-1##":
                print "Authentication failure\n"
                server1.close()
                exit(0)
            elif(len(message)<5):
                print "Try after " + str(message) + " seconds"
                server1.close()
                exit(0)
            elif(message=="logout"):
                print "User logged out"
                server1.close()
                exit(0) 
            elif(message=="User is already online"):
                print "User is already online"
                server1.close()
                exit(0) 
            print message
        else:

            #server1.send(userpass)
            message = sys.stdin.readline()
            server1.send(message)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()

    #i += 1
server1.close()
