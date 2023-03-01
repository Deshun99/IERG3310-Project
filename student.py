import socket
import random
import time

robotVersion = "3.0"
listenPort = 3310
socket.setdefaulttimeout(120)
localhost = ''

# creating socket s1
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s1 connect to server
serverhost = socket.gethostname()
s1.connect((serverhost, listenPort))
s1.send("1155190833".encode())

msg = s1.recv(5)
print("\nData received from Robot: ", msg.decode())

# Converting the bytes object to integer for listenPort
print("\nDoing conversion")
iTCPPort2Connect = int(msg)
# print(iTCPPort2Connect)

s1.close()
######################################################################################

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s2.bind((localhost,iTCPPort2Connect))
s2.listen(1)

print ("\nTCP socket created, ready for listening and accepting connection...")
#print "Waiting for connection on port %(iTCPPort2Connect)s" % locals()
print ("Waiting for connection on port", iTCPPort2Connect)

# accept connections from outside, a new socket is constructed
stuff, address = s2.accept()
serverIP = address[0]
print ("\nClient from %s at port %d connected" %(serverIP,address[1]))

# Close the listen socket
# Usually you can use a loop to accept new connections
s2.close()

newdata = stuff.recv(12)
print("\nEncoded message received: "),
# print(newdata)

print("\nPreparing to decode the message")
n1, n2 = str(newdata).split(",")
iUDPPortRobot = int(n1[2:])
iUDPPortStudent = int(n2[:5])


############################ Completed the decoding message at 4. ##############

# Creating UDP socket to send and receive data
addr = (serverhost, iUDPPortStudent)
s3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s3.bind(addr)

##### Creating the randomised message
randomNumber = str(random.randint(5,10))

s3.sendto(randomNumber.encode(),(serverIP,iUDPPortRobot))
print("\nUDP packet sent!")

####################### Receiving the long message from robot #############

longMsg, addr1 = s3.recvfrom(1024)
decodedStuff = longMsg.decode()

####################### Sending the stuff back to our dear robot ################

for i in range(0,5):
    s3.sendto(str(decodedStuff).encode(),(serverIP,iUDPPortRobot))
    time.sleep(1)
    print ("UDP packet %d sent" %(i+1))

s3.close()