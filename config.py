from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# initializing app and db connection
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:passwordcmp404@cmp404.cokhwcggiflg.eu-west-1.rds.amazonaws.com/cmp404'
application.config['SECRET_KEY'] = "key@to@hash@db@credintials"
db = SQLAlchemy(application)