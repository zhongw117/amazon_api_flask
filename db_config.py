from app import app
from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'abcd@0123'  # home phpmyadmin pw: abcd@0123, office: a
app.config['MYSQL_DATABASE_DB'] = 'amazon_goods'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)