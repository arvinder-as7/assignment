POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = ''
POSTGRES_DB = 'tinyurl'
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}'