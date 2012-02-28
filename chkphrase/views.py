"""
The views module contains all of the flask-driven views that deal with getting
and setting the models of the chkphrase app and returning results in JSON. In
fact, the only function that does not return a jsonified result is the index
controller which renders the index template instead.

The decorators used on the functions should be basically self-explanitory, but
to belabor the point:

@app.route specifies the requested url that invokes the function. This is from
flask and is further documented int flask's documentation.

@auth.requires_auth restricts the invokation to authorized users only. This
decorator is detailed further in the auth module, which should be next to this
one.
"""
from chkphrase import app
from chkphrase import auth
import chkphrase.database as db
from chkphrase.models import User, Category, PreCategory, Genre, Difficulty, Pack, Phrase
from sqlalchemy.exc import IntegrityError
from flask import Flask, request, jsonify, abort, render_template
import hashlib

@app.route('/')
@auth.requires_auth
def index():
    """Render the index page."""
    cur_user = request.authorization.username
    return render_template('index.html', user=cur_user)

@app.route('/users')
@auth.requires_auth
def users():
    """Output a json-encoded list of users. We do not include the password
    hashes for security reasons."""
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
    """Output a json-encoded user corresponding to user_id."""
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
    """Add a user based on the post parameters given and output a json-encoded
    user with the newly given id."""
    cur_user = request.form
    new_user = User(cur_user['name'],
                    cur_user['full_name'],
                    cur_user['password'])
    db.db_session.add(new_user)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(id=new_user.id,
                   name=new_user.name,
                   full_name=new_user.full_name)

@app.route('/users/edit/<int:user_id>', methods=['POST'])
@auth.requires_auth
def edit_user(user_id = None):
    """Update a user based on the post parameters given and output a
    json-encoded user with the new attributes."""
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
        db.db_session.rollback()
        abort(400)
    return jsonify(res)

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@auth.requires_auth
def delete_user(user_id = None):
    """Delete a user with the specifed user_id and return the old name."""
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
    """Return a json-encoded list of all the available categories."""
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
    """Return a json-encoded category corresponding to category_id."""
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
    """Add a new category based on the provided post parameters and return the
    json-encoded result."""
    cur_category = request.form
    new_category = Category(cur_category['name'])
    db.db_session.add(new_category)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(id=new_category.id,
                   name=new_category.name)

@app.route('/categories/edit/<int:category_id>', methods=['POST'])
@auth.requires_auth
def edit_category(category_id = None):
    """Edit a category based on the provided post parameters and return the
    json-encoded result."""
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
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(res)

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
@auth.requires_auth
def delete_category(category_id = None):
    """Delete a category based on category_id and return the old name."""
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
    """Return a json-encoded list of pre-categories."""
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
    """Return a json-encoded pre-category identified by precategory_id."""
    query = db.db_session.query(PreCategory).filter(PreCategory.id ==
                                                    precategory_id)
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
    """Add a new pre-category based on the provided post parameters and return
    the json-encoded result."""
    cur_precategory = request.form
    new_precategory = PreCategory(cur_precategory['name'])
    db.db_session.add(new_precategory)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(id=new_precategory.id,
                   name=new_precategory.name)

@app.route('/precategories/edit/<int:precategory_id>', methods=['POST'])
@auth.requires_auth
def edit_precategory(precategory_id = None):
    """Edit a pre-category based on the provided post parameters and return
    the json-encoded result."""
    query = db.db_session.query(PreCategory).filter(PreCategory.id ==
                                                    precategory_id)
    precategory_data = request.form
    try:
        cur_precategory = query[0]
    except IndexError:
        abort(404)
    res = dict()
    res['name'] = precategory_data['name']
    query.update(res)
    res['id'] =  cur_precategory.id
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(res)

@app.route('/precategories/delete/<int:precategory_id>', methods=['POST'])
@auth.requires_auth
def delete_precategory(precategory_id = None):
    """Delete a pre-category identified by precategory_id and return the former
    name."""
    query = db.db_session.query(PreCategory).filter(PreCategory.id ==
                                                    precategory_id)
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
    """Return a json-encoded list of genres."""
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
    """Return a json-encoded genre identified by the given id."""
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
    """Add a genre based on the given post parameters and return the
    json-encoded result."""
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
    """Edit a genre based on the given post parameters and return the
    json-encoded result."""
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
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    db.db_session.commit()
    return jsonify(res)

@app.route('/genres/delete/<int:genre_id>', methods=['POST'])
@auth.requires_auth
def delete_genre(genre_id = None):
    """Add a genre based on the given id and return the former name."""
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
    """Return a json-encoded list of difficulties."""
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
    """Return a json-encoded difficulty identified by the given id."""
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
    """Add a difficulty based on the given POST parameter and return a
    json-encoded result."""
    cur_difficulty = request.form
    new_difficulty = Difficulty(cur_difficulty['name'])
    db.db_session.add(new_difficulty)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(id=new_difficulty.id,
                   name=new_difficulty.name)

@app.route('/difficulties/edit/<int:difficulty_id>', methods=['POST'])
@auth.requires_auth
def edit_difficulty(difficulty_id = None):
    """Edit a difficulty based on the given POST parameter and return a
    json-encoded result."""
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
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(res)

@app.route('/difficulties/delete/<int:difficulty_id>', methods=['POST'])
@auth.requires_auth
def delete_difficulty(difficulty_id = None):
    """Delete a difficulty based on the given id and return the former name."""
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
    """Return a json-encoded list of packs."""
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
    """Return a json-encoded pack based on the provided id."""
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
    """Add a pack based on the POST parameters and return a json-encoded
    result."""
    cur_pack = request.form
    new_pack = Pack(cur_pack['name'])
    db.db_session.add(new_pack)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(id=new_pack.id,
                   name=new_pack.name)

@app.route('/packs/edit/<int:pack_id>', methods=['POST'])
@auth.requires_auth
def edit_pack(pack_id = None):
    """Edit a pack based on the POST parameters and return a json-encoded
    result."""
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
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    return jsonify(res)

@app.route('/packs/delete/<int:pack_id>', methods=['POST'])
@auth.requires_auth
def delete_pack(pack_id = None):
    """Delete a pack identified by the given id and return the former name."""
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
    """Helper function for outputing phrases. The structure of these nested
    dictionaries is readily converted into json using the flask jsonify
    function."""
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
    """Return a json-encoded list of phrases. This is going to choke and
    probably die once there is a very large database."""
    res = dict()
    query = db.db_session.query(Phrase)
    for cur_phrase in query:
        cur_res = _phrase_to_dict(cur_phrase)
        res[cur_phrase.id] = cur_res
    return jsonify(res)

@app.route('/phrases/<int:phrase_id>')
@auth.requires_auth
def phrase(phrase_id = None):
    """Return a json-encoded phrase identified by the provided id."""
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
    """Add a phrase based on the given post parameters. This function does its
    best to cope with null parameters to categories, precategories, genres,
    etc."""
    cur_phrase = request.form
    new_phrase = Phrase(cur_phrase['phrase'])
    for key, value in cur_phrase.items():
        setattr(new_phrase, key, value)
    db.db_session.add(new_phrase)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    res = _phrase_to_dict(new_phrase)
    return jsonify(res)

@app.route('/phrases/edit/<int:phrase_id>', methods=['POST'])
@auth.requires_auth
def edit_phrase(phrase_id = None):
    """Edit a phrase based on the given post parameters. This function does its
    best to cope with null parameters to categories, precategories, genres,
    etc. To remove associations, pass 'null' as that parameter via POST."""
    query = db.db_session.query(Phrase).filter(Phrase.id==phrase_id)
    phrase_data = request.form
    try:
        cur_phrase = query[0]
    except IndexError:
        abort(404)
    for key, value in phrase_data.items():
        if value.lowercase() == 'null':
            setattr(cur_phrase, key, None)
        else:
            setattr(cur_phrase, key, value)
    db.db_session.add(cur_phrase)
    try:
        db.db_session.commit()
    except IntegrityError:
        db.db_session.rollback()
        abort(400)
    res = _phrase_to_dict(cur_phrase)
    return jsonify(res)

@app.route('/phrases/delete/<int:phrase_id>', methods=['POST'])
@auth.requires_auth
def delete_phrase(phrase_id = None):
    """Delete a phrase identified by the given id and return the former
    phrase."""
    query = db.db_session.query(Phrase).filter(Phrase.id==phrase_id)
    try:
        cur_phrase = query[0]
    except IndexError:
        abort(404)
    str_phrase = cur_phrase.phrase
    db.db_session.delete(cur_phrase)
    db.db_session.commit()
    return jsonify(phrase=str_phrase)

@app.route('/phrases/count')
@auth.requires_auth
def count_phrases():
    """Count all of the phrases in the database."""
    count = db.db_session.query(Phrase).count()
    return jsonify(count=count)
