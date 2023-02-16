import mysql.connector
import hashlib
from os import environ
import base64
import jwt

# These functions need to be implemented
class Token:

    def generate_token(self, username, password):

        cnx = get_db_connection()

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

            token = jwt.encode(payload_data, environ.get("SECRET"), algorithm = "HS256")
        else:
            token = None

        return token

class Restricted:

    def access_data(self, authorization):

        cnx = get_db_connection()

        cursor = cnx.cursor()

        query = ("SELECT role FROM users")

        cursor.execute(query)

        roles = [role[0] for role in cursor.fetchall()]

        cursor.close()
        cnx.close()

        try:
            role = jwt.decode(authorization, environ.get("SECRET"), algorithms=["HS256"])
            if role["role"] in roles:
                return "You are under protected data"
            else:
                return None
        except:
            return None


def get_db_connection():

    try:
        cnx = mysql.connector.connect(
            user = environ.get("DB_USER"),
            password = environ.get("DB_PASS"),
            host = environ.get("DB_HOST"),
            database = environ.get("DB_NAME"))
    except:
        cnx = None

    return cnx