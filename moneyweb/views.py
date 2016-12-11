from moneyweb import app
from moneyweb.database import graph_collection, named_entities_collection
from flask import (
    request, session, redirect,
    url_for, render_template, flash, jsonify,
    send_from_directory,
)
from bson import json_util


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid Username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/graph', methods=['GET', 'PUT'])
def graph_view():
    if request.method == 'PUT':
        update = request.get_json()
        graph_collection.replace_one({}, update, upsert=True)
    graph = graph_collection.find_one({}, {'_id': 0})  # mongo object containing ObjectId
    return jsonify(graph)


@app.route('/named_entities', methods=['GET'])
def named_entities_view():
    named_ents = named_entities_collection.find({}, {'_id': 0})
    ents = [n for n in named_ents]
    return jsonify(ents)


@app.route('/font/<path:path>', methods=['GET'])
def font_view():
    return send_from_directory('font', filename=path)
