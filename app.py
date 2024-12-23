from flask import Flask,render_template,request,redirect,url_for,flash
from flask_security import SQLAlchemyUserDatastore, auth_required, roles_required, roles_accepted, current_user, verify_password, logout_user,login_user
from models import User,Role
from extensions import db,security
from createdata import createData
from createviews import createViews



class LocalDevelopmentConfig():
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SECURITY_PASSWORD_SALT = 'saltypassword'
  SECRET_KEY="myflasksecret"
  SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
  SECURITY_LOGIN_URL= "/login"
  SECURITY_LOGIN_VIEW = None
  DEBUG=True
    
# user_datastore=SQLAlchemyUserDatastore(db,User,Role)

def createApp():
    app = Flask(__name__,template_folder='templates', static_folder='static', static_url_path='/static')
    app.config.from_object(LocalDevelopmentConfig)
     # configure token
    app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authentication-Token'
    app.config['WTF_CSRF_CHECK_DEFAULT'] =False
    app.config['SECURITY_CSRF_PROTECT_MECHANISM'] = []
    app.config['SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS'] = True
    
    app.config["CACHE_TYPE"] = "RedisCache"
    # app.config['CACHE_REDIS_URL'] = "redis://localhost:6379/2"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config['CACHE_REDIS_DB']=2

    
    db.init_app(app)
   
    with app.app_context():
        user_datastore=SQLAlchemyUserDatastore(db,User,Role)
        security.init_app(app,db,user_datastore)

        db.create_all()

        createData(user_datastore)
        createViews(app,user_datastore)
    # connect flask to flask_restful
   
    return app

app=createApp()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()  # Flask-Security logout function
    return redirect(url_for('home'))  # Redirect to home after logout


# @app.route('/users')
# @auth_required()
# def getUsers():
#     return User.query.all()


if __name__=='__main__':
    app.run(port='8080')