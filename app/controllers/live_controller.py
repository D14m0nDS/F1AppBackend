from flask import Blueprint
from app.extensions import socketio
from flask_socketio import emit
from app.services.live_service import LiveService

live_bp = Blueprint('live', __name__, url_prefix='/live')


@live_bp.route('/')
def index():
    return 'Live data broadcasting endpoint'


LiveService.start_live_updates()


@socketio.on('connect', namespace='/live')
def handle_connect():
    emit('message', {'data': 'Connected to live updates'})


@socketio.on('disconnect', namespace='/live')
def handle_disconnect():
    print('Client disconnected')
