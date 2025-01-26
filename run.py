from threading import Thread
from app.utils.broadcasting import broadcast_ip
from app import create_app
from app.extensions import socketio




app = create_app()

if __name__ == '__main__':
    broadcaster_thread = Thread(target=broadcast_ip, daemon=True)
    broadcaster_thread.start()

    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
