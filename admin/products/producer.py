import pika, json
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

params = pika.URLParameters('<url>')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    print("admin: producer: In publish func ")
    channel.basic_publish(
        exchange='',
        routing_key='main', 
        body=json.dumps(body),
        properties=properties
        )
    



