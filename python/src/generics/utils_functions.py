import datetime
import os
from configparser import ConfigParser
import json

import jwt


def get_config_file_data():
    configFilePath:str =  '\\'.join(os.path.abspath(__file__).split('\\')[:3])
    config_file = configFilePath + '\\config.cfg'
    config = ConfigParser()
    return config,config_file

def createJWT(username, secret, authz):
    return jwt.encode({
        'username': username,
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'admin': authz,
        },
        secret,
        algorithm = 'HS256'
        )