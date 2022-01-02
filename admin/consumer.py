import pika, json

params = pika.URLParameters('url')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch, method, properties, body):
    print('received on admin queue after main produced')
    data = json.loads(body)

    if properties.content_type == 'product_liked':
        product = Product.objects.get(id=data)
        product.likes = product.likes + 1
        product.save()
        print("product likes are increased!!")




channel.basic_consume(queue='admin', auto_ack=True, on_message_callback=callback)
print("admin: started consuming")
channel.start_consuming()
channel.close()