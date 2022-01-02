"""
cors documentation: https://flask-cors.readthedocs.io/en/latest/
flask models: https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
example: https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
"""

from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import UniqueConstraint
import requests

from producer import publish

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db/maindb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy(app)
db.init_app(app) 

app = Flask(__name__)

@dataclass
class Product(db.Model):

    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    image = db.Column(db.String(80), unique=True, nullable=False)

@dataclass
class ProductUser(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    UniqueConstraint(user_id, product_id, name='user_product_id_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/like', methods = ['POST'])
def likes(id):

    '''
    bug: here considering product id and user id are same.
    product id and user id has to be fetched from UI
    '''

    url = 'http://docker.for.mac.localhost:8000/api/user/' + str(id)
    req = requests.get(url)
    json_data = req.json()
    print(json_data)

    try:
        product_user = ProductUser(user_id=json_data['id'], product_id=id)
        db.session.add(product_user)
        db.session.commit()
        publish("product_liked", id)

    except:
        abort(400, "you already liked this product")

    return "success"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
