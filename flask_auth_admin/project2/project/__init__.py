from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#from models.py import User


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__,template_folder='templates', static_folder='static')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Admin

    @login_manager.user_loader
    def load_user(admin_id):
        # since the admin_id is just the primary key of our user table, use it in the query for the user
        return Admin.query.get(int(admin_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

app = create_app()
app.app_context().push()
db.create_all()
