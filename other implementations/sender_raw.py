import socket

# Sender settings
host = '10.38.1.118'
port = 12345

# Create a socket object
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input for the message
    # message = input('Enter a message (type "exit" to quit): ')
    message="hello"
    # Check if the user wants to exit
    if message.lower() == 'exit':
        break

    # Encode and send the messadfge to the receiver
    sender_socket.sendto(message.encode('utf-8'), (host, port))
    # print debug
    print(f'Message sent to {host}:{port}')

# Close the socket when done
sender_socket.close()
