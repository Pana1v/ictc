import socket

def get_ip_address_and_port():
    try:
        # Create a socket and connect to an external server (e.g., Google's public DNS)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        
        # Choose a port to check for availability (you can modify this to your desired range)
        start_port = 12345
        end_port = 65535
        port = start_port
        while port <= end_port:
            try:
                # Try binding to the selected port
                s.bind((ip_address, port))
                break
            except socket.error:
                # If the port is not available, try the next one
                port += 1

        s.close()
        return ip_address, port
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    result = get_ip_address_and_port()
    if isinstance(result, tuple) and len(result) == 2:
        ip_address, port = result
        print(f"Your IP address is: {ip_address}")
        print(f"An open port on your machine is: {port}")
    else:
        print(result)
