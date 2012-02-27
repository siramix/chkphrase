from chkphrase import app
from chkphrase import auth
import chkphrase.database as db
from chkphrase.models import User
from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify, abort
import hashlib

@app.route('/')
@auth.requires_auth
def index():
    return 'Hello World! %s' % request.authorization.username

@app.route('/users')
@app.route('/users/')
@auth.requires_auth
def users():
    res = dict()
    allUsers = db.db_session.query(User)
    for user in allUsers:
        curRes = dict()
        curRes['id'] = user.id
        curRes['name'] = user.name
        curRes['full_name'] = user.full_name
        res[user.id] = curRes
    return jsonify(res)

@app.route('/users/<int:user_id>')
@auth.requires_auth
def user(user_id = None):
    allUsers = db.db_session.query(User).filter(User.id==user_id)
    try:
        curUser = allUsers[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = curUser.id
    res['name'] = curUser.name
    res['full_name'] = curUser.full_name
    return jsonify(res)

@app.route('/users/add', methods=['POST'])
@auth.requires_auth
def add_user():
    cur_user = request.form
    new_user = User(cur_user['name'],
                    cur_user['full_name'],
                    cur_user['password'])
    db.db_session.add(new_user)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_user.id,
                   name=new_user.name,
                   full_name=new_user.full_name)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
@auth.requires_auth
def edit_user(user_id = None):
    query = db.db_session.query(User).filter(User.id==user_id)
    user_data = request.form
    try:
        cur_user = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = user_data['name']
    res['full_name'] = user_data['full_name']
    res['password'] = hashlib.sha256(user_data['password']).hexdigest()
    query.update(res)
    res['id'] =  cur_user.id
    del res['password']
    return jsonify(res)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@auth.requires_auth
def delete_user(user_id = None):
    query = db.db_session.query(User).filter(User.id==user_id)
    try:
        cur_user = query[0]
    except IndexError:
        abort(404)
    name = cur_user.name
    db.db_session.delete(cur_user)
    db.db_session.commit()
    return jsonify(name=name)
