# Summary: This code defines a UDP client that allows the user to select between local or broadcast network.
# To send the equipment code to the server, call get_equipment_code(equipment_code).
# Where do I call get_equipment_code()? Call it from another script where you want to send the code.

# Importations
import socket

# Function to select a server network


def select_network():
    while True:
        print("Select the server network to connect to: ")
        print("1. Local Network (Default)")
        print("2. Select personalized network")
        choice = input("Select option (1 or 2): ")

        # Switch statement (match in python)
        match choice:
            case '1':
                return ("127.0.0.1", 7501)
            case '2':
                address = input("Enter you network address: ")
                return (address, 7501)
            case _:
                print("Invalid choice. Try again.\n")
                print("----------------------------\n")


# Function to get equipment code and handle any future logic.
def get_equipment_code(equipment_code):
    code = equipment_code

    # Add future logic to validate code, such as check if digit, save to database, etc.

    # Send code to server
    send_packet(code)
    return code

# This function gets the data, encodes it, creates a UDP socket, and send the data


def send_packet(data):
    # variable containing the message to send to the server
    msgFromClient = data

    # Encode the message to bytes!
    bytesToSend = str.encode(msgFromClient)

    # Creates a tuple with IP address and port number of server
    # Changed from 127.0.0.1 (localhost) to broadcast address
    serverAddressPort = select_network()

    # Defines the buffer size at 1KB or 1024 bytes
    bufferSize = 1024

    # Create a UDP socket at client side (socket() is a class from socket module, creates object)
    UDPClientSocket = socket.socket(
        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # enable broadcasts
    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send to server using created UDP socket
    UDPClientSocket.sendto(bytesToSend, serverAddressPort)

    # Receive response from server
    msgFromServer = UDPClientSocket.recvfrom(bufferSize)
    msg = "Message from Server {}".format(msgFromServer[0])

    # Print message from server
    print(msg)

    print("Server address port:  ", serverAddressPort)
