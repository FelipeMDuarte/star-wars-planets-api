import os


class Config:
    SERVICE_NAME = os.environ.get('SERVICE_NAME')
    DEPENDENCY_API_A_URL = os.environ.get('DEPENDENCY_API_A_URL')
    DEPENDENCY_API_B_URL = os.environ.get('DEPENDENCY_API_B_URL')


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
