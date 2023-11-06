from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.mundane import Mundane
from flask_app.models.user import User


@app.route('/mund/new')
def new_mund():
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('mund_new.html', user=user)

@app.route('/mund/new/post', methods=['POST'])
def new_mund_post():
    if 'user_id' not in session:
        return redirect('/user/login')
    if not Mundane.validate_mund(request.form):
        return redirect('/mund/new')

    data = {
        'id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'price': request.form['price'],
        'user_id': session['user_id']
    }
    Mundane.save(data)
    return redirect('/dashboard')



@app.route('/mund/<int:id>')
def mund_details(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('mund_view.html',user=user,mundane=Mundane.get_by_id({'id': id}))


@app.route('/mund/buy/<int:id>')
def buy_mund(id):
    if 'user_id' not in session:
        return redirect('/user/login')
    user = User.get_by_id({"id":session['user_id']})
    if not user:
        return redirect('/user/logout')
    return render_template('m_items.html',user=user,  mundane=Mundane.get_by_id({'id': id}))

@app.route('/mund/destroy/<int:id>')
def sold(id):
    if 'user_id' not in session:
        return redirect('/user/login')

    Mundane.destroy({'id':id})
    return redirect('/dashboard')