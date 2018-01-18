# -*- coding:utf-8 -*-
from datetime import timedelta
class Config(object):
    SECRET_KEY = "Ay98Cct2oNSlnHDdTl8"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class LastConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/dbtest"

    ###celery
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    CELERYBEAT_SCHEDULE = {
        'getOrder':{
            'task':'app.tasks.getIrobotboxOrder',
            "schedule": timedelta(seconds=60),
        },
        'checkOrder':{
            'task':'app.tasks.getOrderAgain',
            "schedule": timedelta(seconds=30),
        }

    }


class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/test_data"


config = {'default':LastConfig, 'test':TestConfig}