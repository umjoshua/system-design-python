import pika
import os
import json
import tempfile
from bson.objectid import ObjectId
import moviepy.editor as mp

def convert(message, fs_videos, fs_audios, channel):
    message = json.loads(message)
    tf = tempfile.NamedTemporaryFile()
    vf = fs_videos.get(ObjectId(message["video_fid"]))
    tf.write(vf.read())
    audio = mp.VideoFileClip(tf.name).audio
    tf.close()
    
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)
    
    f = open(tf_path,"rb")
    data = f.read()
    fid = fs_audios.put(data)
    f.close()
    os.remove(tf_path)

    
    message["audio_fid"] = str(fid)

    try:
        channel.basic_publish(
            exchange = "",
            routing_key = os.environ.get("AUDIO_QUEUE"),
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as e:
        fs_audios.delete(fid)
        return "Failed to publish"