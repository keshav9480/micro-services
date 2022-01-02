import pika, json
from main import Product, db

params = pika.URLParameters('amqps://zearquzz:KafE1jw2BUEEi9TBlWt3q2Pajs3TfFRU@puffin.rmq2.cloudamqp.com/zearquzz')
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='main')

def callback(ch, method, properties, body):
    print('received from main queue')
    data = json.loads(body)
    print("data: ",data)

    '''
    drawback:
    cannot add duplicate entry with same title and image name. both the attributes must be unique
    '''
    
    if properties.content_type == 'product_created':
        print("received in main queue from admin queue")
        print("product created after admin produced product")
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == 'product_updated':
        print("product created after admin produced product")
        product = Product.query.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.add(product)
        db.session.commit()

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
    
channel.basic_consume(queue='main', auto_ack=True, on_message_callback=callback)
print("main: started consuming")
channel.start_consuming()
channel.close()