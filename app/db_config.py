from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Welcome1'
app.config['MYSQL_DATABASE_DB'] = 'campusdb'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)