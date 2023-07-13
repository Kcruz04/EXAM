# userss.py
from exam_app import app
from flask import render_template,redirect,request,session,flash
from exam_app.models.user_model import User


@app.route('/')
def index():
    return render_template("login_reg.html")


@app.route('/register', methods=['POST'])
def register():
    # if not User.validate_user(request.form):
        # we redirect to the template with the form.
        print(request.form)
        if not User.validate(request.form):
            return redirect('/')
        
        User.register(request.form)
        # ... do other things
        return redirect('/tv_shows')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    valid_email = User.login(request.form)
    if valid_email:
        session['uid'] = valid_email.id
        return redirect('/tv_shows')
    else:
        return redirect('/')
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')  


#Recieves requests from client direct to  show, edit, or delete and pages

