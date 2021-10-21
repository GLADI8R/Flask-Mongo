from todo.extensions import mongo
from flask import Blueprint, render_template, redirect, url_for, request
from bson.objectid import ObjectId


main = Blueprint('main', __name__)


@main.route('/')
def index():
    todos = mongo.db.pyTodoDB
    todos = todos.find()
    return render_template('index.html', todos=todos)


@main.route('/add_todo', methods=["POST"])
def add_todo():
    todos = mongo.db.pyTodoDB
    newItem = request.form.get('add-todo')
    todos.insert_one({'text': newItem, 'completed': False})
    return redirect(url_for('main.index'))


@main.route('/complete_todo/<oid>')
def complete_todo(oid):
    todos = mongo.db.pyTodoDB
    item = todos.find_one({'_id': ObjectId(oid)})
    item['completed'] = True
    return redirect(url_for('main.index'))


@main.route('/delete_completed')
def delete_completed():
    todos = mongo.db.pyTodoDB
    todos.delete_many({'completed': True})
    return redirect(url_for('main.index'))


@main.route('/delete_all')
def delete_all():
    todos = mongo.db.pyTodoDB
    todos.delete_many({})
    return redirect(url_for('main.index'))
