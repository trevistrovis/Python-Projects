from flask_app import app
from flask_app.models import user, tree
from flask import render_template, redirect, session, request


@app.route('/dashboard')
def dashboard():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session["user_id"]
    }
    get_user = user.User.get_id(data)
    return render_template('dashboard.html', user = get_user, all_trees = tree.Tree.add_users_to_trees())

@app.route('/new/tree')
def create_tree():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session["user_id"]
    }
    return render_template('new_tree.html', user = user.User.get_id(data))

@app.route('/user/account')
def view_my_trees():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session["user_id"]
    }
    return render_template('my_trees.html', this_user = user.User.get_all_trees_by_user(data))

@app.route('/edit/<int:id>')
def edit_tree(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    return render_template('edit_tree.html', this_tree = tree.Tree.get_one_tree(data))

@app.route('/show/<int:id>')
def view_a_tree(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    return render_template('show_tree.html', this_tree = tree.Tree.get_one_tree(data))

@app.route('/delete/<int:id>')
def delete_tree(id):
    data = {
        
        "id" : id
    }
    tree.Tree.delete_tree(data)
    return redirect('/user/account')

@app.route('/plant', methods = ["POST"])
def plant_tree():
    if not tree.Tree.validate_tree(request.form):
        return redirect('/new/tree')
    data = {
        "species" : request.form["species"],
        "location" : request.form["location"],
        "reason" : request.form["reason"],
        "date_planted" : request.form["date_planted"],
        "user_id" : session["user_id"]
    }
    tree.Tree.create_tree(data)
    return redirect('/dashboard')

@app.route('/update/<int:id>', methods = ["POST"])
def update_tree(id):
    if not tree.Tree.validate_tree(request.form):
            return redirect('/new/tree')
    data = {
        "species" : request.form["species"],
        "location" : request.form["location"],
        "reason" : request.form["reason"],
        "date_planted" : request.form["date_planted"],
        "id" : id
    }
    tree.Tree.edit_tree(data)
    return redirect('/dashboard')
