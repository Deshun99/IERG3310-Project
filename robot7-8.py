# IERG3310 Project
# first version written by FENG, Shen Cody
# second version modified by YOU, Lizhao
# Third version modified by Jonathan Liang @ 2016.10.25

import socket
import random
import time

robotVersion = "3.0"
listenPort = 3310
socket.setdefaulttimeout(120)
localhost = ''

print ("Robot version " + robotVersion + " started")
print ("You are reminded to check for the latest available version")

print ("")

# Create a TCP socket to listen connection
print ("Creating TCP socket...")
listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listenSocket.bind((localhost, listenPort))
listenSocket.listen(5)
print ("Done")

print ("\nTCP socket created, ready for listening and accepting connection...")
#print "Waiting for connection on port %(listenPort)s" % locals()
print ("Waiting for connection on port", listenPort)

# accept connections from outside, a new socket is constructed
s1, address = listenSocket.accept()
studentIP = address[0]
print ("\nClient from %s at port %d connected" %(studentIP,address[1]))
# Close the listen socket
# Usually you can use a loop to accept new connections
listenSocket.close()

data = s1.recv(10)
print ("Student ID received: " ),
print(data.decode())

iTCPPort2Connect = random.randint(0,9999) + 20000
print ("Requesting STUDENT to accept TCP <%d>..." %iTCPPort2Connect)

s1.send(str(iTCPPort2Connect).encode())
print ("Done")

time.sleep(1)
print ("\nConnecting to the STUDENT s1 <%d>..." %iTCPPort2Connect)

############################################################################# phase 1
# Connect to the server (student s2)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((studentIP,iTCPPort2Connect))

print("Done\n")

# (step 7) obtaining buffer size from student
bufferSize = s2.recv(10)
bufferSize = bufferSize.decode()[1:]
print("Buffer-size information from student = ", bufferSize)

longMSG = "Mari kita rakyat Singapura"
size = 0
i = 0

print("Proceeding to send message over to buffer size <%d>" % (int(bufferSize)))

start_time = time.time()
end_time = start_time + 30

while(time.time() <= end_time) :
     s2.send(longMSG.encode())
     size += len(longMSG)
     i += 1

print("Number of sent messages: <%d>, Total sent bytes: <%d>.\n" % (i, size))

time.sleep(1)
# (step 8) repeating step 7 with changing receiver buffer size 

for k in range(0, 8):
    bufferSize = s2.recv(10)
    bufferSize = bufferSize.decode()[1:]
    print('Buffer Size of Student = ', bufferSize)
    message = longMSG

    i = 0 # Number of received messages
    size = 0 # messages size

    print("Proceeding to send message over to buffer size <%d> " % (int(bufferSize)))
    start_time = time.time()
    end_time = start_time + 30

    while (time.time() <= end_time):
        s2.send(message.encode())
        i += 1
        size += len(message)
    print("Number of sent messages: <%d>, Total sent bytes: <%d>.\n" % (i, size))

s1.close()
s2.close()
exit()
