class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'angel'
    MYSQL_PASSWORD = '23002280'
    MYSQL_DB = 'api_utl'
    MYSQL_CURSORCLASS = 'Cursor'  

config = {
    'development': DevelopmentConfig
}