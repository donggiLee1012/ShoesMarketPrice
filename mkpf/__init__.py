from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .views import market_views,model_views,auth_views,platform_views,shoes_views
    app.register_blueprint(market_views.bp)
    app.register_blueprint(model_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(platform_views.bp)
    app.register_blueprint(shoes_views.bp)

    # 필터
    from .filter import format_datetime, exchange_rate
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['price'] = exchange_rate


    return app