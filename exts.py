from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
# from flask_bootstrap import Bootstrap

csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
dropzone = Dropzone()
socketio = SocketIO()
# bootstrap = Bootstrap()


class ValidationError(ValueError):
    pass
