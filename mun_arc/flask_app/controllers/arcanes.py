from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.arcane import Arcane
from flask_app.models.mundane import Mundane
from flask_app.models.user import User

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
        
    return render_template('dashboard.html', user=user, arcanes=Arcane.get_all(), mundanes=Mundane.get_all())

@app.route('/arc/new')
def new_arc():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('arc_new.html', user=user)

@app.route('/arc/new/post', methods=['POST'])
def new_arc_post():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Arcane.validate_arc(request.form):
        return redirect('/arc/new')

    data = {
        'id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'type': request.form['type'],
        'user_id': session['user_id']
    }
    Arcane.save(data)
    return redirect('/dashboard')

@app.route('/arc/<int:id>')
def arc_details(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('arc_view.html',user=user,arcane=Arcane.get_by_id({'id': id}))

@app.route('/arc/edit/<int:id>')
def change_specifis(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('arc_edit.html',user=user,  arcane=Arcane.get_by_id({'id': id}))

@app.route('/arc/edit/process/<int:id>', methods=['POST'])
def post_changes(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Arcane.validate_arc(request.form):
        return redirect(f'/arc/edit/{id}')

    data = {
        'id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'type': request.form['type'],
        'user_id': session['user_id']
        
    }
    Arcane.update(data)
    return redirect('/dashboard')

@app.route('/arc/buy/<int:id>')# lets users change their enchantment
def buy(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('items.html',user=user,  arcane=Arcane.get_by_id({'id': id}))


@app.route('/arc/destroy/<int:id>')# removes item from inventory once purchased
def purchased(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Arcane.destroy({'id':id})
    return redirect('/dashboard')

