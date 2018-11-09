import os


class Config:
    SERVICE_NAME = os.environ.get('SERVICE_NAME')
    MONGO_URI = os.environ.get('MONGO_URI')


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
