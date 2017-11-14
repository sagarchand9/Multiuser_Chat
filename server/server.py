import os
import socket
import select
import sys
import datetime
from thread import *
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
 
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

server.bind((IP_address, Port))
server.listen(100)
 
list_of_clients = []
client_last_hr = {}
conn_user={}
user_tries={} 
IP_tries={} 

def clientthread(conn, addr,client_user):
    conn.send("Welcome to this chatroom!")
 
    while True:
            client_last_hr[client_user]=datetime.datetime.now()
            try:
                message = conn.recv(2048)
                PorB = message[:5]
                
                if message:
                    #print len(list_of_clients)
                    if(PorB == "broad"):
                        message = message[10:]
                        #print IP_user
                        #print conn_IP
                        print "<" + client_user + "> " + message
 						
                        message_to_send = "<" + client_user + "> " + message
                        broadcast(message_to_send, conn)
                   	
                    
                    elif(PorB == "messa"):
                        recipient = message[8:]
                        i=0
                        while(recipient[i]!=' '):
                            i=i+1
 						
                        message = recipient[i+1:]
                        recipient = recipient[:i]
                        message_to_send = "<" + client_user + "> " + message
                        message_sender = client_user
                        p2p(message_sender, message_to_send, conn, recipient)
 					
                    elif(PorB == "whoel"):
                        whoel(conn)
                    
                    elif(PorB == "whola"):
                    	whola(conn)

                    elif(PorB == "logou"):
                        conn.send("logout")
                        remove(conn)    
                        return                    
                    elif(PorB == "block"):
                        recpt = message[6:]
                        #print recpt
                        recpt = recpt.split()[0]
                        #print recpt
                        #print "Hello"
                        #print recpt + str(len(recpt))
                        block(client_user,recpt)
                    elif(PorB == "unblo"):
                        recpt = message[8:]
                        recpt = recpt.split()[0]
                        #print recpt + str(len(recpt))
                        unblock(client_user, recpt) 

                            	
                else:
                    """ if the connection is broken"""
                    remove(conn)
                    return
            except:
                continue

def whola(connection):
    print len(client_last_hr)
    now=datetime.datetime.now()
    a=''
    #print(client_last_hr)
    for clients in client_last_hr:
    	#print "int"
    	
    	#print (now-client_last_hr[clients]).seconds
        if ((now-client_last_hr[clients]).seconds)<60*60:
            #print "bhejo"
            #print conn_IP
            #print conn_user
            a=a+clients+"\n"
        	#connection.send(clients+"\n")
            #print clients[1]
    connection.send(a)
            
def whoel(connection):
    print len(list_of_clients)
    a=''
    for clients in list_of_clients:
        if clients!=connection:
            #print conn_IP
            #print conn_user
            a=a+conn_user[clients]+"\n"
            #connection.send(conn_user[clients]+"\n")
            
            #print clients[1]
    connection.send(a)
                    

def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
                remove(clients)

def p2p(message_sender, message, connection, recipient):
    rec_online=0

    flag_for_block_check = 0
    with open("blocked_user.txt","r+") as f:
        for line in f:
            blocked_by, blocked_user = line.split()
            if(message_sender == blocked_by and recipient == blocked_user) or (recipient == blocked_by and message_sender == blocked_user):
                connection.send("private messages are blocked")
                return

    for clients in list_of_clients:
        if clients!=connection:
            if(conn_user[clients]==recipient):
                try:
                    clients.send(message)
                    rec_online = 1
                except:
                    clients.close()
                    remove(clients)
                    
    if rec_online == 0:
        flag_for_recipient = 0
        with open("users.txt", "r") as f:
            for line in f:
                str1 = line.split()[0]
                if str1 == recipient:
                    flag_for_recipient = 1

        if not flag_for_recipient == 1:
            connection.send(recipient + " does not exit")
        else:
            f = open("stored_message.txt","a+")
            f.write(recipient+","+message_sender+","+message)
            f.close()
            print "recipient is offline, message is saved" 

def block(blocked_by, blocked_user):
    flag_for_pair_found = 0
    with open("blocked_user.txt","r+") as f:
        for line in f:
            u1, u2 = line.split()
            if(u1 == blocked_by and u2 == blocked_user):
                flag_for_pair_found = 1
                break

        if flag_for_pair_found == 0:
            f.write(blocked_by + " " + blocked_user+"\n")
            print "pair <" + blocked_by + ", " + blocked_user + "> is saved in blocked file"

def unblock(blocked_by, blocked_user):
    temp_file = "temp_" +  blocked_by +".txt"
    block_file = "blocked_user.txt"
    flag_to_check = 0
    with open(block_file, "r+") as f, open(temp_file, "w") as outfile:
        for line in f:
            u1, u2 = line.split()
            if(u1 == blocked_by and u2 == blocked_user):
                print "pair <" + blocked_by + ", " + blocked_user + "> is removed from blocked file"
            else:
                flag_to_check = 1
                outfile.write(line)

    if flag_to_check == 1:
        try:
            os.rename(temp_file, block_file)
        except WindowsError:
            os.remove(block_file)
            os.rename(temp_file, block_file)
    else:
        os.remove(temp_file)


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
 
while True:
    conn, addr = server.accept()
    #list_of_clients.append((conn,addr[0]))
    already_online=0
    mes = conn.recv(2048)

    client_user, client_pass = mes.split(":",1)

    found = False
    if client_user in user_tries:
        if(user_tries[client_user][0]==3):
            if((datetime.datetime.now() - user_tries[client_user][1]).seconds<60):
                conn.send(str(60 - (datetime.datetime.now() - user_tries[client_user][1]).seconds))
                remove(conn)
                continue
            else:
                user_tries[client_user][0]==0
    	
    with open("users.txt", "r") as f:
        for line in f:
            str1 = line.split()[0]
            if  str1 == client_user:
                str2 = line.split()[1]
                if str2 == client_pass:
                    found = True
                    user_tries[client_user]=(0,datetime.datetime.now())
                    break

    if not found:
        conn.send("-1##")
        if client_user not in user_tries:
            user_tries[client_user]=(1,datetime.datetime.now())
        else:
            user_tries[client_user]=(user_tries[client_user][0]+1,datetime.datetime.now())
        				
        remove(conn)
        continue
	
	
	
    for clients in list_of_clients:
        if conn_user[clients]==client_user:
            already_online=1
            break
    if(already_online==1):
    	conn.send("User is already online")
        remove(conn)
    	continue

    print "New user <" + client_user + "> connected with IP " + addr[0]
    #conn_IP[conn]=addr[0]
    #IP_user[addr[0]]=client_user
    conn_user[conn]=client_user 
    client_last_hr[client_user]=datetime.datetime.now()


    temp_file = "temp_"+client_user+".txt"
    message_file = "stored_message.txt"
    flag_to_check = 0
    with open(message_file, "r+") as f, open(temp_file, "w") as outfile:
    #f = open("stored_message.txt", "r+")
        for line in f:
            stored_mes = line.split(',',2)
            if(client_user == stored_mes[0]):
                conn.send(stored_mes[2])
            else:
                flag_to_check = 1
                outfile.write(line)
    if flag_to_check == 1:
        try:
            os.rename(temp_file, message_file)
        except WindowsError:
            os.remove(message_file)
            os.rename(temp_file, message_file)
    else:
        os.remove(temp_file)
    #print conn
    #print addr[0]
    #print "sasas"
    #print conn_IP
    #print IP_user
    # creates and individual thread for every user 
    # that connects
    
    
    
    list_of_clients.append(conn) 
    start_new_thread(clientthread,(conn,addr,client_user))    

conn.close()
server.close()
