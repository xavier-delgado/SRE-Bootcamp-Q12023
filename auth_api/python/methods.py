import mysql.connector
import hashlib
from os import environ
import jwt

# These functions need to be implemented
class Token:

    def generate_token(self, username, password):
        cnx = mysql.connector.connect(
            user = environ.get("DB_USER"),
            password = environ.get("DB_PASS"),
            host = environ.get("DB_HOST"),
            database = environ.get("DB_NAME"))

        cursor = cnx.cursor()

        query = ("SELECT password, salt, role FROM users WHERE username = '{}'".format(username))

        cursor.execute(query)

        encrypted_password, salt, role = cursor.fetchone()

        cursor.close()
        cnx.close()

        salted_password = "{}{}".format(password, salt)

        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()

        if hashed_password == encrypted_password:
            payload_data = {
                "role": role
                }

            token = jwt.encode(
                payload = payload_data,
                key = environ.get("SECRET"),
                algorithm = "HS256")
        else:
            token = None

        return token

class Restricted:

    def access_data(self, authorization):
        return 'test'
