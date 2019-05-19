from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from app.redis_rate_limiter import RateLimiter

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db.create_all()
rate_limiter = RateLimiter()
cors = CORS(app)

from app import routes
