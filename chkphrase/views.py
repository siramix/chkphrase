from chkphrase import app
from chkphrase import auth
import chkphrase.database as db
from chkphrase.models import User, Category, PreCategory, Genre, Difficulty, Pack, Phrase
from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify, abort
import hashlib

@app.route('/')
@auth.requires_auth
def index():
    return 'Hello World! %s' % request.authorization.username

@app.route('/users')
@auth.requires_auth
def users():
    res = dict()
    query = db.db_session.query(User)
    for cur_user in query:
        cur_res = dict()
        cur_res['id'] = cur_user.id
        cur_res['name'] = cur_user.name
        cur_res['full_name'] = cur_user.full_name
        res[cur_user.id] = cur_res
    return jsonify(res)

@app.route('/users/<int:user_id>')
@auth.requires_auth
def user(user_id = None):
    query = db.db_session.query(User).filter(User.id==user_id)
    try:
        cur_user = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_user.id
    res['name'] = cur_user.name
    res['full_name'] = cur_user.full_name
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
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
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

@app.route('/categories')
@auth.requires_auth
def categories():
    res = dict()
    query = db.db_session.query(Category)
    for cur_category in query:
        cur_res = dict()
        cur_res['id'] = cur_category.id
        cur_res['name'] = cur_category.name
        res[cur_category.id] = cur_res
    return jsonify(res)

@app.route('/categories/<int:category_id>')
@auth.requires_auth
def category(category_id = None):
    query = db.db_session.query(Category).filter(Category.id==category_id)
    try:
        cur_category = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_category.id
    res['name'] = cur_category.name
    return jsonify(res)

@app.route('/categories/add', methods=['POST'])
@auth.requires_auth
def add_category():
    cur_category = request.form
    new_category = Category(cur_category['name'])
    db.db_session.add(new_category)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_category.id,
                   name=new_category.name)

@app.route('/categories/edit/<int:category_id>', methods=['POST'])
@auth.requires_auth
def edit_category(category_id = None):
    query = db.db_session.query(Category).filter(Category.id==category_id)
    category_data = request.form
    try:
        cur_category = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = category_data['name']
    query.update(res)
    res['id'] =  cur_category.id
    db.db_session.commit()
    return jsonify(res)

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
@auth.requires_auth
def delete_category(category_id = None):
    query = db.db_session.query(Category).filter(Category.id==category_id)
    try:
        cur_category = query[0]
    except IndexError:
        abort(404)
    name = cur_category.name
    db.db_session.delete(cur_category)
    db.db_session.commit()
    return jsonify(name=name)

@app.route('/precategories')
@auth.requires_auth
def precategories():
    res = dict()
    query = db.db_session.query(PreCategory)
    for cur_precategory in query:
        cur_res = dict()
        cur_res['id'] = cur_precategory.id
        cur_res['name'] = cur_precategory.name
        res[cur_precategory.id] = cur_res
    return jsonify(res)

@app.route('/precategories/<int:precategory_id>')
@auth.requires_auth
def precategory(precategory_id = None):
    query = db.db_session.query(PreCategory).filter(PreCategory.id==precategory_id)
    try:
        cur_precategory = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_precategory.id
    res['name'] = cur_precategory.name
    return jsonify(res)

@app.route('/precategories/add', methods=['POST'])
@auth.requires_auth
def add_precategory():
    cur_precategory = request.form
    new_precategory = PreCategory(cur_precategory['name'])
    db.db_session.add(new_precategory)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_precategory.id,
                   name=new_precategory.name)

@app.route('/precategories/edit/<int:precategory_id>', methods=['POST'])
@auth.requires_auth
def edit_precategory(precategory_id = None):
    query = db.db_session.query(PreCategory).filter(PreCategory.id==precategory_id)
    precategory_data = request.form
    try:
        cur_precategory = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = precategory_data['name']
    query.update(res)
    res['id'] =  cur_precategory.id
    db.db_session.commit()
    return jsonify(res)

@app.route('/precategories/delete/<int:precategory_id>', methods=['POST'])
@auth.requires_auth
def delete_precategory(precategory_id = None):
    query = db.db_session.query(PreCategory).filter(PreCategory.id==precategory_id)
    try:
        cur_precategory = query[0]
    except IndexError:
        abort(404)
    name = cur_precategory.name
    db.db_session.delete(cur_precategory)
    db.db_session.commit()
    return jsonify(name=name)

@app.route('/genres')
@auth.requires_auth
def genres():
    res = dict()
    query = db.db_session.query(Genre)
    for cur_genre in query:
        cur_res = dict()
        cur_res['id'] = cur_genre.id
        cur_res['name'] = cur_genre.name
        res[cur_genre.id] = cur_res
    return jsonify(res)

@app.route('/genres/<int:genre_id>')
@auth.requires_auth
def genre(genre_id = None):
    query = db.db_session.query(Genre).filter(Genre.id==genre_id)
    try:
        cur_genre = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_genre.id
    res['name'] = cur_genre.name
    return jsonify(res)

@app.route('/genres/add', methods=['POST'])
@auth.requires_auth
def add_genre():
    cur_genre = request.form
    new_genre = Genre(cur_genre['name'])
    db.db_session.add(new_genre)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_genre.id,
                   name=new_genre.name)

@app.route('/genres/edit/<int:genre_id>', methods=['POST'])
@auth.requires_auth
def edit_genre(genre_id = None):
    query = db.db_session.query(Genre).filter(Genre.id==genre_id)
    genre_data = request.form
    try:
        cur_genre = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = genre_data['name']
    query.update(res)
    res['id'] =  cur_genre.id
    db.db_session.commit()
    return jsonify(res)

@app.route('/genres/delete/<int:genre_id>', methods=['POST'])
@auth.requires_auth
def delete_genre(genre_id = None):
    query = db.db_session.query(Genre).filter(Genre.id==genre_id)
    try:
        cur_genre = query[0]
    except IndexError:
        abort(404)
    name = cur_genre.name
    db.db_session.delete(cur_genre)
    db.db_session.commit()
    return jsonify(name=name)

@app.route('/difficulties')
@auth.requires_auth
def difficulties():
    res = dict()
    query = db.db_session.query(Difficulty)
    for cur_difficulty in query:
        cur_res = dict()
        cur_res['id'] = cur_difficulty.id
        cur_res['name'] = cur_difficulty.name
        res[cur_difficulty.id] = cur_res
    return jsonify(res)

@app.route('/difficulties/<int:difficulty_id>')
@auth.requires_auth
def difficulty(difficulty_id = None):
    query = db.db_session.query(Difficulty).filter(Difficulty.id==difficulty_id)
    try:
        cur_difficulty = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_difficulty.id
    res['name'] = cur_difficulty.name
    return jsonify(res)

@app.route('/difficulties/add', methods=['POST'])
@auth.requires_auth
def add_difficulty():
    cur_difficulty = request.form
    new_difficulty = Difficulty(cur_difficulty['name'])
    db.db_session.add(new_difficulty)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_difficulty.id,
                   name=new_difficulty.name)

@app.route('/difficulties/edit/<int:difficulty_id>', methods=['POST'])
@auth.requires_auth
def edit_difficulty(difficulty_id = None):
    query = db.db_session.query(Difficulty).filter(Difficulty.id==difficulty_id)
    difficulty_data = request.form
    try:
        cur_difficulty = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = difficulty_data['name']
    query.update(res)
    res['id'] =  cur_difficulty.id
    db.db_session.commit()
    return jsonify(res)

@app.route('/difficulties/delete/<int:difficulty_id>', methods=['POST'])
@auth.requires_auth
def delete_difficulty(difficulty_id = None):
    query = db.db_session.query(Difficulty).filter(Difficulty.id==difficulty_id)
    try:
        cur_difficulty = query[0]
    except IndexError:
        abort(404)
    name = cur_difficulty.name
    db.db_session.delete(cur_difficulty)
    db.db_session.commit()
    return jsonify(name=name)

@app.route('/packs')
@auth.requires_auth
def packs():
    res = dict()
    query = db.db_session.query(Pack)
    for cur_pack in query:
        cur_res = dict()
        cur_res['id'] = cur_pack.id
        cur_res['name'] = cur_pack.name
        res[cur_pack.id] = cur_res
    return jsonify(res)

@app.route('/packs/<int:pack_id>')
@auth.requires_auth
def pack(pack_id = None):
    query = db.db_session.query(Pack).filter(Pack.id==pack_id)
    try:
        cur_pack = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['id'] = cur_pack.id
    res['name'] = cur_pack.name
    return jsonify(res)

@app.route('/packs/add', methods=['POST'])
@auth.requires_auth
def add_pack():
    cur_pack = request.form
    new_pack = Pack(cur_pack['name'])
    db.db_session.add(new_pack)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    return jsonify(id=new_pack.id,
                   name=new_pack.name)

@app.route('/packs/edit/<int:pack_id>', methods=['POST'])
@auth.requires_auth
def edit_pack(pack_id = None):
    query = db.db_session.query(Pack).filter(Pack.id==pack_id)
    pack_data = request.form
    try:
        cur_pack = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = pack_data['name']
    query.update(res)
    res['id'] =  cur_pack.id
    db.db_session.commit()
    return jsonify(res)

@app.route('/packs/delete/<int:pack_id>', methods=['POST'])
@auth.requires_auth
def delete_pack(pack_id = None):
    query = db.db_session.query(Pack).filter(Pack.id==pack_id)
    try:
        cur_pack = query[0]
    except IndexError:
        abort(404)
    name = cur_pack.name
    db.db_session.delete(cur_pack)
    db.db_session.commit()
    return jsonify(name=name)

def _phrase_to_dict(cur_phrase):
    """Helper function for outputing phrases."""
    cur_res = dict()
    cur_res['id'] = cur_phrase.id
    cur_res['phrase'] = cur_phrase.phrase
    cur_res['source'] = cur_phrase.source
    cur_res['approved'] = cur_phrase.approved
    cur_res['user'] = dict()
    if cur_phrase.user != None:
        cur_res['user']['id'] = cur_phrase.user.id
        cur_res['user']['name'] = cur_phrase.user.name
    cur_res['pre_category'] = dict()
    if cur_phrase.pre_category != None:
        cur_res['pre_category']['id'] = cur_phrase.pre_category.id
        cur_res['pre_category']['name'] = cur_phrase.pre_category.name
    cur_res['genre'] = dict()
    if cur_phrase.genre != None:
        cur_res['genre']['id'] = cur_phrase.genre.id
        cur_res['genre']['name'] = cur_phrase.genre.name
    cur_res['category'] = dict()
    if cur_phrase.category != None:
        cur_res['category']['id'] = cur_phrase.category.id
        cur_res['category']['name'] = cur_phrase.category.name
    cur_res['difficulty'] = dict()
    if cur_phrase.difficulty != None:
        cur_res['difficulty']['id'] = cur_phrase.difficulty.id
        cur_res['difficulty']['name'] = cur_phrase.difficulty.name
    cur_res['pack'] = dict()
    if cur_phrase.pack != None:
        cur_res['pack']['id'] = cur_phrase.pack.id
        cur_res['pack']['name'] = cur_phrase.pack.name
    return cur_res

@app.route('/phrases')
@auth.requires_auth
def phrases():
    res = dict()
    query = db.db_session.query(Phrase)
    for cur_phrase in query:
        cur_res = _phrase_to_dict(cur_phrase)
        res[cur_phrase.id] = cur_res
    return jsonify(res)

@app.route('/phrases/<int:phrase_id>')
@auth.requires_auth
def phrase(phrase_id = None):
    query = db.db_session.query(Phrase).filter(Phrase.id==phrase_id)
    try:
        cur_phrase = query[0]
    except IndexError:
        abort(404)
    res = _phrase_to_dict(cur_phrase)
    return jsonify(res)

@app.route('/phrases/add', methods=['POST'])
@auth.requires_auth
def add_phrase():
    cur_phrase = request.form
    new_phrase = Phrase(cur_phrase['phrase'])
    db.db_session.add(new_phrase)
    try:
        db.db_session.commit()
    except IntegrityError:
        abort(400)
    res = _phrase_to_dict(new_phrase)
    return jsonify(res)

@app.route('/phrases/edit/<int:phrase_id>', methods=['POST'])
@auth.requires_auth
def edit_phrase(phrase_id = None):
    query = db.db_session.query(Phrase).filter(Phrase.id==phrase_id)
    phrase_data = request.form
    try:
        cur_phrase = query[0]
    except IndexError:
        abort(404)
    new_values = dict()
    new_values['phrase'] = phrase_data['phrase']
    query.update(new_values)
    db.db_session.commit()
    res = _phrase_to_dict(cur_phrase)
    return jsonify(res)

@app.route('/phrases/delete/<int:phrase_id>', methods=['POST'])
@auth.requires_auth
def delete_phrase(phrase_id = None):
    query = db.db_session.query(Phrase).filter(Phrase.id==phrase_id)
    try:
        cur_phrase = query[0]
    except IndexError:
        abort(404)
    str_phrase = cur_phrase.phrase
    db.db_session.delete(cur_phrase)
    db.db_session.commit()
    return jsonify(phrase=str_phrase)
