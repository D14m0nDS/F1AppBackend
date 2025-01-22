from threading import Thread
import socket as socket
import time
from app import create_app
from app.extensions import socketio

def broadcast_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        try:
            # Broadcast the Flask app's IP address
            ip = "192.168.1.5"
            message = f"flask_backend:{ip}:5000"
            s.sendto(message.encode('utf-8'), ('<broadcast>', 5000))
            print(f"Broadcasting IP: {ip}")
            time.sleep(5)  # Broadcast every 5 seconds
        except Exception as e:
            print(f"Broadcasting error: {e}")

app = create_app()

if __name__ == '__main__':
    # Run the broadcaster in a separate thread
    broadcaster_thread = Thread(target=broadcast_ip, daemon=True)
    broadcaster_thread.start()

    # Start the Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)