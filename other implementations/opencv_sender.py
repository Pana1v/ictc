import socket

# Sender settings
host = '192.168.144.152'
port = 12345

# Create a socket object
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input for the message
    message = input('Enter a message (type "exit" to quit): ')

    # Check if the user wants to exit
    if message.lower() == 'exit':
        break

    # Encode and send the message to the receiver
    sender_socket.sendto(message.encode('utf-8'), (host, port))

# Close the socket when done
sender_socket.close()
