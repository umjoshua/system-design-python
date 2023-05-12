import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
from waitress import serve

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://mongodb-svc/videos"

mongo_video = PyMongo(server, uri="mongodb://mongodb-svc/videos")
mongo_audio = PyMongo(server, uri="mongodb://mongodb-svc/audios")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_audios = gridfs.GridFS(mongo_audio.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq-svc"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err

@server.route("/upload",methods=["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return err
    
    access = json.loads(access) 

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly 1 file is required", 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)
            
            if err:
                return err
            
        return "Success", 200
    else:
        return "Unauthorized", 401

@server.route("/download",methods=["GET"])
def download():
    access, err = validate.token(request)
    if err:
        return err
    
    access = json.loads(access)
    if access["admin"]:
        fid = request.args.get("fid")
        
        if not fid:
            return "fid required", 400
        
        try:
            output = fs_audios.get(ObjectId(fid))
            return send_file(output, download_name=f"{fid}.mp3")
        
        except Exception as e:
            print(e)
            return "Internal server error", 500
    
    return "unauthorized", 401

if __name__ == "__main__":
    serve(server,host="0.0.0.0",port = 8080) 