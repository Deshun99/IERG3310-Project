import socket
import random
import time
import numpy as np

robotVersion = "3.0"
listenPort = 3310
socket.setdefaulttimeout(120)
localhost = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), listenPort))
s.send(bytes("1155190833", "utf-8"))

msg = s.recv(1024)
print("\nMessage received from Robot: ")
# print(msg)

# Converting the bytes object to integer for listenPort
print("\nDoing conversion")
iTCPPort2Connect = int(msg)
# print(iTCPPort2Connect)

s.close()
######################################################################################

studentIP = socket.gethostname()
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.bind((studentIP,iTCPPort2Connect))
s1.listen(1)

s2, address = s1.accept()
serverIP = address[0]
s1.close()
print("Student connected with robot")

#buffer size
bufferSize = s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print('Buffer size = ', str(bufferSize))

# (step 7) sending buffer size to server(Robot)
sendingBufferSize = "b" + str(bufferSize)
s2.send(sendingBufferSize.encode())

# receiving large number of messages from Robot

# Number of received messages
i = 0  

# size of messages
size = 0  

print("Receiving message of buffer size <%d>" % bufferSize)
start_time = time.time()
end_time = start_time + 30
while (time.time() <= end_time):
    recivedMessage = s2.recv(10)
    recivedMessage = recivedMessage.decode()
    size += len(recivedMessage)
    i += 1
print("Number of received messages: <%d>, Total received bytes: <%d>.\n" % (i, size))

time.sleep(1)

# (step 8) repeating step 7 with changing receiver buffer size 
buffer = np.array([10, 50, 100, 500, 2000, 5000, 10000, 20000])

for varBufferSize in buffer:
    print('Buffer size = ', str(varBufferSize))
    send_buffer_size = "b" + str(varBufferSize)
    s2.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, varBufferSize)
    s2.send(send_buffer_size.encode())
   
    i = 0   # Number of received messages
    size = 0 # messages size

    print("Receiving message of buffer size <%d>" % (s2.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)))
    start = time.time()
    while (time.time() - start) <= 30:
        receivedMessage = s2.recv(10)
        size += len(receivedMessage)
        receivedMessage = receivedMessage.decode()
        i += 1
    print("Number of received messages: <%d>, Total received bytes: <%d>.\n" % (i, size))

time.sleep(1)

# Close the listen socket
# Usually you can use a loop to accept new connections
s1.close()
s2.close()
exit()