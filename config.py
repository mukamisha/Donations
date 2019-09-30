import os

class Config:

    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    # MOVIE_API_BASE_URL ='https://api.themoviedb.org/3/movie/{}?api_key={}'
    # MOVIE_API_KEY = '2197098f34dd6b61e8919f32ae43e37d'
    SECRET_KEY = 'jacky2'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mukamisha:mukamisha@97@localhost/pitch'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mukamisha:mukamisha@97@localhost/pitch_test'
class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mukamisha:mukamisha@97@localhost/pitch'
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig

}




