from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from src.models import user, role, permission, user_role, role_permission, item, item_category, farmer_rating
from src.models.Model import db
from src.app import app

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
