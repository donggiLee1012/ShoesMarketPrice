from flask import Flask,render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()
migrate = Migrate()

def page_not_found(e):
    return render_template('404.html'),404

def server_error(e):
    return render_template('500.html'), 500

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    from .views import market_views,model_views,auth_views,platform_views,shoes_views,main_views
    app.register_blueprint(market_views.bp)
    app.register_blueprint(main_views.bp)
    app.register_blueprint(model_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(platform_views.bp)
    app.register_blueprint(shoes_views.bp)

    # 필터
    from .filter import format_datetime, exchange_rate,format_datetime_detail,format_datetime_hour,whattype,integer,maxlength,roles
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['datetime_detail'] = format_datetime_detail
    app.jinja_env.filters['price'] = exchange_rate
    app.jinja_env.filters['datetime_hour'] = format_datetime_hour
    app.jinja_env.filters['type'] = whattype
    app.jinja_env.filters['int'] = integer
    app.jinja_env.filters['maxstr'] = maxlength
    app.jinja_env.filters['roles'] = roles

    # 오류페이지
    app.register_error_handler(404,page_not_found)
    app.register_error_handler(500, server_error)

    return app