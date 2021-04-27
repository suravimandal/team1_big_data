class Config(object):
    DEBUG=True
    UPLOAD_FOLDER = 'UPLOADS'
    SECRET_KEY = 'yhjfyvjuyetcuyfuyjvkutgkigukjgbkg'
    DB_HOST = 'localhost'
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASS = 'password'
class ProductionConfig(Config):
    DEBUG=False
    UPLOAD_FOLDER = 'UPLOADS'
    SECRET_KEY = 'yhjfyvjuyetcuyfuyjvkutgkigukjgbkg'
    DB_HOST = 'localhost'
    DB_NAME = 'postgres'
    DB_USER = 'postgres'
    DB_PASS = 'mysecretpassword'
class DevelopmentConfig(Config):
    pass
    
