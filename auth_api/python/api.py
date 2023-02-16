from flask import Flask
from flask import jsonify, abort
from flask import request
from methods import Token, Restricted

app = Flask(__name__)
login = Token()
protected = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']

    token = login.generate_token(username, password)

    if token is None:
        abort(403)

    res = {
        "data": token
    }

    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')

    jwt = auth_token.split()

    response = protected.access_data(jwt[1])

    if response is None:
        abort(403)

    res = {
        "data": response
    }

    return jsonify(res)

@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
