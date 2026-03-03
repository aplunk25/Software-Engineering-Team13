# Summary: This code defines a UDP client that allows the user to select between local or broadcast network.

# To send the equipment code to the server, call get_equipment_code(equipment_code).

# Where do I call get_equipment_code()? Call it from another script where you want to send the code.


# Importations

import socket


# Global variable to store server address

SERVER_ADDRESS = None


# Function to select a server network


def select_network():

    while True:

        print("Select the server network to connect to: ")

        print("1. Local Network (Default)")

        print("2. Select personalized network")

        choice = input("Select option (1 or 2): ")

        # Switch statement (match in python)

        if choice == '1':

            return ("127.0.0.1", 7501)

        elif choice == '2':

            address = input("Enter you network address: ")

            return (address, 7501)

        else:

            print("Invalid choice. Try again.\n")

            print("----------------------------\n")

# Configure server once at startup and store in global variable


def configure_server():
    global SERVER_ADDRESS
    SERVER_ADDRESS = select_network()


# Function to get equipment code and handle any future logic.

def get_equipment_code(equipment_code):

    code = equipment_code

    # Add future logic to validate code, such as check if digit, save to database, etc.

    # Send code to server

    send_packet(code)

    return code


# This function gets the data, encodes it, creates a UDP socket, and send the data


def send_packet(data):

    # Check if the server address is configured, else prints error and returns
    if SERVER_ADDRESS is None:
        print("ERROR: Server address not configured.")
        return

    # variable containing the message to send to the server

    msgFromClient = data

    # Encode the message to bytes!

    bytesToSend = str.encode(msgFromClient)

    # Defines the buffer size at 1KB or 1024 bytes

    bufferSize = 1024

    # Create a UDP socket at client side (socket() is a class from socket module, creates object)

    UDPClientSocket = socket.socket(

        family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # enable broadcasts

    UDPClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send to server using created UDP socket

    UDPClientSocket.sendto(bytesToSend, SERVER_ADDRESS)

    # Receive response from server

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    # decode the bytes to a normal string
    msg_decoded = msgFromServer[0].decode()

    # now format the message
    msg = "Message from Server: {}".format(msg_decoded)

    # Print message from server

    print(msg)

    print("Server address port:  ", SERVER_ADDRESS[1])
