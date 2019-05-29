import os

from flask_migrate import upgrade, Migrate
from src import create_app, db

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.cli.command()
def deploy() -> None:
    upgrade()
