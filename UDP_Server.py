# UDP Server Script to listen for incoming UPD packets.

# Problems: What confirmation message should the server send? Probably the same message it received or the equipment code.

import socket

localIP = "0.0.0.0"
localPort = 7501
broadcastPort = 7500
bufferSize = 1024
msgFromServer = None
# bytesToSend = str.encode(msgFromServer)

# Create a datagram socket for localPort
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Create a datagram socket for broadcastPort
UDPBroadcastSocket = socket.socket(
    family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

# Bind address to broadcast port
UDPBroadcastSocket.bind((localIP, broadcastPort))


print("UDP server up and listening")

# Listen for incoming datagrams

while (True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP = "Client IP Address:{}".format(address)

    print(clientMsg)
    print(clientIP)

    # Prepare reply message
    msgFromServer = clientMsg
    bytesToSend = str.encode(msgFromServer)

    # Sending a reply to client
    UDPBroadcastSocket.sendto(bytesToSend, address)
