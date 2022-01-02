import pika

params = pika.URLParameters('url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(method, body):
    
    properties = pika.BasicProperties(method)
    print("main:producer: In publish func ")
    channel.basic_publish(
        exchange='',
        routing_key='admin', 
        body=json.dumps(body),
        properties=properties
        )

