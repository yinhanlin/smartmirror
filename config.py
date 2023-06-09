import os
# 数据库配置信息
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "XXXXXXf"
DATABASE = "smartmirror"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "XXXXXXXX@qq.com"
MAIL_PASSWORD = "XXXXXXXXXbhjf"
MAIL_DEFAULT_SENDER = "XXXXXXXX@qq.com"

# Dropzone配置
DROPZONE_MAX_FILE_SIZE = 3
DROPZONE_MAX_FILES = 30
MAX_CONTENT_LENGTH = 3 * 1024 * 1024
DROPZONE_ALLOWED_FILE_TYPE = 'image'
DROPZONE_ENABLE_CSRF = True

# 图片配置
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CLOTH_UPLOAD_PATH = os.path.join(basedir, 'FrontendDevelop/static/images/uploads')
