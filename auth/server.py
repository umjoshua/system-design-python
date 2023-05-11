import jwt
import os
import datetime
from flask import Flask, request
from flask_mysqldb import MySQL
from waitress import serve


server = Flask(__name__)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

mysql = MySQL(server)

@server.route("/login",methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401
    cur = mysql.connection.cursor()
    res=cur.execute("SELECT email,password FROM user WHERE email=%s",(auth.username))
    username="tester@gmail.com"
    res=cur.execute("SELECT email,password FROM user WHERE email=%s",(username,))
    print(res)
    if res>0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        print(email)

        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        else:
            return CreateJWT(auth.username,os.getenv("JWT_SECRET"),True)
    else:
        return "invalid credentials", 401

@server.route("/validate",methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401
    
    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.getenv("JWT_SECRET"),algorithm=["H256"]
        )
    except:
        return "not authorized", 401
    
    return decoded, 200

def CreateJWT(username,secret,authz):
    return jwt.encode(
        {
            "username":username,
            "exp":datetime.datetime.now(tz=datetime.timezone.utc)+datetime.timedelta(days=1),
            "iat":datetime.datetime.utcnow(),
            "admin":authz,
        },
        secret,
        algorithm="HS256",
    )

if __name__ == "__main__":
    serve(server,host="0.0.0.0",port=5000) 