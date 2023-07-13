from exam_app import app
from flask import render_template,redirect,request,session,flash
from exam_app.models.tv_show_model import Tv_show
from exam_app.models.user_model import User


@app.route("/tv_shows")
def tv_shows():
    if not 'uid' in session:
        return redirect('/')
    # call the get all classmethod to get all shows
    tv_shows = Tv_show.tv_shows_with_users()
    user = User.get_one(session['uid'])
    print(tv_shows)
    # return results
    return render_template("shows.html", tv_shows=tv_shows, user = user)

# relevant code snippet from server.py
#This takes the anchor tag to create a new user and returns creat.html

@app.route('/add_show')
def new_tv_show():
    if not 'uid' in session:
        return redirect('/')
    return render_template("add_show.html")

@app.route('/create_show', methods=["POST"])
def create_tv_show():
    if not 'uid' in session:
        return redirect('/')
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "title" : request.form["title"],
        "network" : request.form["network"],
        "release_date" : request.form["release_date"],
        "description" : request.form["description"],
        "user_id" : request.form["user_id"]
    }
    print(request.form)
    # We pass the data dictionary into the save method from the User class.
    Tv_show.save(data)
    #If values in html are same as in db we can use
    #@app.route('/friends/create', methods=['POST'])
    # def create_friend():
    #     Friend.save(request.form)
    #     return redirect('/')
    # Don't forget to redirect after saving to the database.
    return redirect('/tv_shows')
    
@app.route('/one_show/<int:id>')
def one_tv_show(id):
    tv_show = Tv_show.get_one(id)
    tv_shows = Tv_show.tv_shows_with_users()
    user = User.get_one(session['uid'])
    return render_template("one_show.html", tv_show = tv_show, user = user, tv_shows=tv_shows)

@app.route('/edit_show/<int:id>')
def edit_tv_show(id):
    if not 'uid' in session:
        return redirect('/')
    # tv_show = Tv_show.get_one(id)
    return render_template("edit_show.html", tv_show = Tv_show.get_one(id))

@app.route('/update_show', methods = ["POST"])
def update_tv_show():
    if not 'uid' in session:
        return redirect('/')
    print(request.form)
    Tv_show.update(request.form)
    return redirect('/tv_shows')

@app.route('/delete_show/<int:id>')
def delete_tv_show(id):
    print(id)
    Tv_show.delete(id)
    return redirect('/tv_shows')


#Recieves requests from client direct to  show, edit, or delete and pages