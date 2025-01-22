import socket

def listen_for_broadcast(port=5000):
    """Listen for UDP broadcast messages."""
    try:
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", port))  # Bind to all network interfaces on the specified port

        print(f"Listening for broadcasts on port {port}...")
        while True:
            data, addr = sock.recvfrom(1024)  # Buffer size is 1024 bytes
            print(f"Received message: {data.decode()} from {addr}")
    except KeyboardInterrupt:
        print("\nStopped listening.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    listen_for_broadcast()
