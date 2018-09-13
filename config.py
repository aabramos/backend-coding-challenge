

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '86xd8Zx94xd7x12o}x18f28f517xbf14c9ba1bx81b888ui1ortbb4'

    POSTGRES = {
        'user': 'postgres',
        'pw': 'postgres',
        'db': 'unbabel_database',
        'host': 'localhost',
        'port': '5432',
    }

    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Unbabel API
    URL = 'https://sandbox.unbabel.com/tapi/v2/translation/'
    HEADERS = {
        'Authorization': 'ApiKey fullstack-challenge:9db71b322d43a6ac0f681784ebdcc6409bb83359',
        'Content-Type': 'application/json',
    }
