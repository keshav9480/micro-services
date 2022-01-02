from main import app, db
from main import Product, ProductUser
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

db.init_app(app)
db.create_all()

if __name__ == '__main__':
    manager.run()
