from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.like import Like
from flask_app.models import user
from flask_app.models.show import Show

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("This page is only available to logged in users.")
        return redirect("/")
    shows = Show.get_all_shows()
    user_id = {
        'user_id' : session['user_id']
    }
    like = Show.get_creator_likes(user_id)
    unliked = Show.get_other_shows(user_id)
    print(unliked)
    return render_template("dashboard.html", shows = shows, like = like, unliked = unliked)

@app.route("/shows/new")
def new_show():
    return render_template("create.html")

@app.route("/shows/create", methods=['POST'])
def create_show():
    if Show.validate_show(request.form):
        data = {
            'title': request.form['title'],
            'network' : request.form['network'],
            'release_date': request.form['release_date'],
            'description': request.form['description'],
            'user_id': session['user_id'],
            'first_name' : session['first_name'],
            'last_name' : session['last_name']
        }
        Show.create_new_show(data)
        return redirect("/dashboard")
    else:
        return redirect('/shows/new')

@app.route("/shows/<int:shows_id>")
def view_description(shows_id):
    data = {
        'shows_id': shows_id
    }
    show = Show.view_description(data)
    creator = Show.get_show_creator(data)
    return render_template("view_description.html", show = show, creator = creator)

@app.route("/shows/edit/<int:shows_id>")
def edit_show(shows_id):
    data = {
        'shows_id': shows_id
    }
    show = Show.view_description(data)
    return render_template("edit_show.html", show = show)

@app.route("/show/edit/<int:shows_id>", methods=["POST"])
def update_show(shows_id):
    if Show.validate_show(request.form):
        data = {
            'id': shows_id,
            'title': request.form['title'],
            'network': request.form['network'],
            'release_date': request.form['release_date'],
            'description': request.form['description'],
            'user_id': session['user_id']
        }
        Show.update_show(data)
        return redirect('/dashboard')
    else:
        return redirect(f"/shows/edit/{shows_id}")

@app.route('/shows/<int:shows_id>/delete')
def delete_show(shows_id):
    data = {
        'id': shows_id
    }
    Show.delete_show(data)
    return redirect('/dashboard')

@app.route('/add/like/<int:shows_id>')
def add_like(shows_id):
    data = {
        'users_id' : session['user_id'],
        'shows_id' : shows_id
    }
    Like.add_like(data)
    return redirect("/dashboard")

@app.route("/delete/like/<shows_id>")
def delete_like(shows_id):
    data = {
        'users_id' : session['user_id'],
        'shows_id': shows_id
    }
    Like.delete_like(data)
    return redirect("/dashboard")