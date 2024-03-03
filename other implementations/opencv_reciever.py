import socket

# Receiver settings
host = '10.38.1.118'
port = 12345

# Create a socket object
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
receiver_socket.bind((host, port))

print('Receiver waiting for messages...')

while True:
    # Receive data from the sender
    data, addr = receiver_socket.recvfrom(1024)

    # Decode and print the received message
    message = data.decode('utf-8')
    print(f'Received message: {message} from {addr}')
