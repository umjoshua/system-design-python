import pika
import sys
import os
import time
from pymongo import MongoClient
import gridfs
from convert import to_audio


def main():
    client = MongoClient("mongodb://mongodb-svc", 27017)
    mongo_video = client.videos
    mongo_audio = client.audios

    fs_videos = gridfs.GridFS(mongo_video)
    fs_audios = gridfs.GridFS(mongo_audio)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq-svc")
        )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = to_audio.convert(body, fs_videos, fs_audios, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_consume(queue=os.environ.get("VIDEO_QUEUE"),on_message_callback=callback)
    
    channel.start_consuming()
    

if __name__ == "__main__":
    main()