
from flask import Flask,request,redirect,url_for,flash,render_template
from flask_security import SQLAlchemyUserDatastore, auth_required, roles_required, roles_accepted, current_user, verify_password, logout_user,login_user
from models import User

def createViews(app,user_datastore:SQLAlchemyUserDatastore):
    
    @app.route('/mylogin',methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            print("Email",email)
            # Find the user based on email
            user = user_datastore.find_user(email=email)
            
            # Check if user exists and password is correct
            if user and verify_password(password, user.password):
                # login_user(user)  # Log the user in
                flash("You Are Logegd In")
                return render_template('admindashboard.html',userdata=user)  # Redirect to home after login
            else:
                # If credentials are incorrect, return an error message or re-render the login form
                return "Invalid credentials", 401
        
        # If GET request, just show the login page
        return render_template('login.html')
    
    
    @app.route('/getusers')
    @auth_required()
    def getUsers():
        users=User.query.all()
        user = current_user
        return render_template('admindashboard.html',userdata=user,users=users)