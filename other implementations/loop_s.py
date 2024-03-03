import socket

# Receiver settings (use loopback address for testing on the same machine)
host = '192.168.144.152'
port = 12345

# Create a socket object
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        message = input('Enter a message (type "exit" to quit): ')
        if message.lower() == 'exit':
            break
        sender_socket.sendto(message.encode('utf-8'), (host, port))

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the socket when done
    sender_socket.close()
