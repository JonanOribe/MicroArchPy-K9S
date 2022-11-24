import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
from utils_functions import createJWT,get_config_file_data

config,config_file = get_config_file_data()
config.read(config_file)

MYSQL_HOST:str = ''#config._defaults['MYSQL_HOST']
MYSQL_USER:str = ''#config._defaults['MYSQL_USER']
MYSQL_PASSWORD:str = ''#config._defaults['MYSQL_PASSWORD']
MYSQL_DB:str = ''#config._defaults['MYSQL_DB']
MYSQL_PORT:str = ''#config._defaults['MYSQL_PORT']
JWT_SECRET:str = ''#config._defaults['JWT_SECRET']

server = Flask(__name__)
mysql = MySQL(server)

@server.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return 'missing credentials',401
    #check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        'SELECT email, password FROM user WHERE email=%s',
        (auth.username,auth.password)
    )

    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return 'Invalid credentials',401
        else:
            return createJWT(auth.username, JWT_SECRET, True)
    else:
        return 'Invalid credentials',401

@server.route('/validate',methods=['POST'])
def validate():
    encoded_jwt = request.headers['Authorization']

    if not encoded_jwt:
        return 'Missing credentials',401

    encoded_jwt = encoded_jwt.split(' ')[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, JWT_SECRET, algorithms=['HS256']
        )
    except:
        return 'Not authorized'

    return decoded, 200

if __name__ == '__main__':
    server.run(host='0.0.0.0',port=5000)