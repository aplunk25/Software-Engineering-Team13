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
    
# Allow immediate reuse of address
UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UDPBroadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

# Bind address to broadcast port
UDPBroadcastSocket.bind((localIP, broadcastPort))


print("UDP server up and listening")

# Listen for incoming datagrams

while (True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message_bytes = bytesAddressPair[0]
    address = bytesAddressPair[1]
    
    # Decode bytes to string
    message = message_bytes.decode()
    
    clientMsg = "Client Message: {}".format(message)
    clientIP = "Client IP Address: {}".format(address)

    print(clientMsg)
    print(clientIP)

    # Prepare reply message
    msgFromServer = clientMsg
    bytesToSend = str.encode(msgFromServer)

    # Sending a reply to client
    UDPBroadcastSocket.sendto(bytesToSend, address)
