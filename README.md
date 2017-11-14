Developed a comprehensive client-server messaging application which has-

• basic security features of a chat room

• support for broadcast and point to point messages

• concepts of asynchronous messaging


Server folder contains file server.py which should be run as "python <IP> <port>" 

It also contains 3 txt files-

--"users.txt"  contains list of users and their passwords

--"blocked_user.txt" contains list of users and usrs blocked by them

--"stored_message.txt" contains messages recieved by user when he/she was offline. These messages are then sent to him when he comes back 
online again, thus including concept of asynchronous messaging.

Client folder contains a file client.py which should be run as "python <IP> <port> <user>:<password>"



ARCHITECTURE

Server is turned on a particular IP and port number. Clients connect to this IP and port.

• Security - No user can log in twice. 3 failed login attempts, blocks that user for 60 sec. He/she cannot
connect to server during this time.
Once user has connected to server, he/she has list features which he/she can avail of. Following list presents
Messaging features-

• Broadcast - type ”broadcast <message>” and message goes to all online users

• Private message - type ”message <user><message>” and message goes to the particular user. Concept
of asynchronous messaging is used here. If user is online, message goes immediately to him/her. If not, then
message is stored in a file and sent to the user whenever he/she come online next(and message is deleted
from that file)

• Block and Unblock - type ”block <user>” to block a user. type ”unblock <user>” to block a user. – The
users can block and unblock other user(s) Based on this the private messages will be delivered
Other features have also been implemented-

• Logout-User also has option of logging out. By typing ”logout” he would be logged out.

• whoelse - By typing ”whoelse”, user can know all other users who are currently online with him

• wholasthr: By typing ”wholasthr”, user can know all other users who were connected within last hour.
