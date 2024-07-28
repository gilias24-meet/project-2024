from flask import Flask
from flask import Flask, render_template, request, url_for, redirect
from flask import session as login_session
import random
import pyrebase

app = Flask(__name__)
app = Flask(__name__, template_folder='templates', static_folder='static')

                                    
firebaseConfig = {
  'apiKey': "AIzaSyAAL4ipnYtGe8RGsmH4VUgs5RYwgP64X_Y",
  'authDomain': "giftapp-ad937.firebaseapp.com",
  'databaseURL': "https://giftapp-ad937-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "giftapp-ad937",
  'storageBucket': "giftapp-ad937.appspot.com",
  'messagingSenderId': "904198728084",
  'appId': "1:904198728084:web:05542fc6834719046fc781",
  'measurementId': "G-G8HJ6XR7YP"
}

firebase = pyrebase.initialize_app(firebaseConfig) 
auth = firebase.auth()
db = firebase.database()

app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def signup():
  if request.method == "GET": 
    return render_template("signup.html")
  else:
    try:
      email = request.form["email"]
      username = request.form['username']
      passwored = request.form['passwored']
      login_session["user"] = auth.create_user_with_email_and_password(email, passwored)
      user = {'username': username, 'email':email, 'passwored':passwored }
      UID = login_session["user"]['localId']
      db.child("user").child(UID).set(user)


      return render_template("home.html")
    except Exception as e:
      print(e)
      return render_template("signup.html")

@app.route('/login',methods=['GET', 'POST'])
def login():
  if request.method == "GET": 
    return render_template("login.html")

  else:
    email = request.form["email"]
    username = request.form['username']
    passwored = request.form['passwored']
    login_session["user"] = auth.sign_in_with_email_and_password(email, passwored)

    user = {'username': username, 'email':email, 'passwored':passwored }
    UID = login_session["user"]['localId']
      
    db.child("user").child(UID).set(user)

    return render_template("home.html")
  
@app.route('/home', methods = ['GET','POST'])
def home():
   return render_template("home.html")

@app.route('/food', methods = ['GET','POST'])
def food():
   return render_template("food.html")


@app.route('/your_idea', methods = ['GET','POST'])
def your_idea():
  if request.method == "POST":
    print("dffddf")
    story = request.form["story"]  
    db.child("stories").push(story)
    return redirect(url_for("story"))
  return render_template("your_idea.html")

@app.route('/clothes', methods = ['GET','POST'])
def clothes():
  return render_template("clothes.html")

@app.route('/wrappers', methods = ['GET','POST'])
def wrappers():
   return render_template("wrappers.html")

@app.route('/creative', methods = ['GET','POST'])
def creative():
   return render_template("creative.html")

@app.route('/story', methods=['GET', 'POST'])
def story():
  stories = db.child('stories').get().val()
  return render_template("story.html", story=stories)

if __name__ == '__main__':
    app.run(debug = True, port='2000')


