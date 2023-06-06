from flask import Flask
import config
from exts import db, mail, dropzone, csrf, socketio
from blueprints.ClothChange import bp as clo_bp
from blueprints.DisInformation import bp as in_bp
from apis.v1 import api_v1
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
app.config['SECRET_KEY'] = 'AASDFASDF'
db.init_app(app)
mail.init_app(app)
dropzone.init_app(app)
# bootstrap.init_app(app)
csrf.init_app(app)
csrf.exempt(api_v1)
csrf.exempt(in_bp)
socketio.init_app(app)

migrate = Migrate(app, db)
# 蓝图注册关联
# blueprints:模块化
app.register_blueprint(clo_bp)
app.register_blueprint(in_bp)
app.register_blueprint(api_v1, url_prefix='/api/v1')
# app.register_blueprint(api_v1, subdomain='api', url_prefix='/api/v1')

if __name__ == '__main__':
    app.debug = True
    # app.config['SERVER_NAME'] = 'tingfeng.online:2023'
    # app.run(host='0.0.0.0')
    app.run(host='0.0.0.0', port=2023)
