# migrate.py

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import app, db  # assuming app and db are defined in app.py

# Initialize Flask-Script and Flask-Migrate
migrate = Migrate(app, db)
manager = Manager(app)

# Add migrate command to manager
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
