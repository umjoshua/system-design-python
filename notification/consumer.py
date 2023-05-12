import pika
import sys
import os
import time
from send import email

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("rabbitmq-svc")
        )
    channel = connection.channel()

    def callback(ch, method, properties, body):
        err = email.send(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_consume(queue=os.environ.get("AUDIO_QUEUE"),on_message_callback=callback)
    
    channel.start_consuming()
    

if __name__ == "__main__":
    main()