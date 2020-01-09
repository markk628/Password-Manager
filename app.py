from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from passwordgen import generate_password
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/passwordmanager')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
accounts = db.accounts
names = db.names
accounts.drop()

app = Flask(__name__)

# names page
@app.route('/')
def person_name():
    return render_template('person_name.html', names=names.find())

# new Person page
@app.route('/new')
def person_new():
    return render_template('person_new.html', name={}, title='New Person')

# submitting the new person to database
@app.route('/', methods=['POST'])
def person_submit():
    name = {
        'name': request.form.get('name')
    }
    print(name)
    name_id = names.insert_one(name).inserted_id
    return redirect(url_for('person_show', name_id=name_id))

# individual person page
@app.route('/<name_id>')
def person_show(name_id):
    name = names.find_one({'_id': ObjectId(name_id)})
    return render_template('person_show.html', name=name)

# code for editing person's name
@app.route('/<name_id>', methods=['POST'])
def person_update(name_id):
    updated_person = {
        'name': request.form.get('name')
    }
    names.update_one(
        {'_id': ObjectId(name_id)},
        {'$set': updated_name})
    return redirect(url_for('person_show', name_id=name_id))

# edit person's name route
@app.route('/<name_id>/edit')
def person_edit(namee_id):
    name = names.find_one({'_id': ObjectId(name_id)})
    return render_template('person_edit.html', name=name, title='Edit Name')

# delete route for person
@app.route('/<name_id>/delete', methods=['POST'])
def pereson_delete(name_id):
    names.delete_one({'_id': ObjectId(name_id)})
    return redirect(url_for('person_name'))






# home page
@app.route('/')
def pm_index():
    return render_template('pm_index.html', accounts=accounts.find())

# password generator page
@app.route('/accounts/generate')
def pm_generate():
    password = generate_password()
    return render_template('pm_generate.html', password=password)

# new account page
@app.route('/accounts/new')
def account_new():
    return render_template('pm_new.html', account={}, title='New Account')

# submitting the new account to database
@app.route('/accounts', methods=['POST'])
def account_submit():
    account = {
        'platform': request.form.get('platform'),
        'id': request.form.get('id'),
        'password': request.form.get('password'),
        'url': request.form.get('url')
    }
    print(account)
    account_id = accounts.insert_one(account).inserted_id
    return redirect(url_for('account_show', account_id=account_id))

# account page
@app.route('/accounts/<account_id>')
def account_show(account_id):
    account = accounts.find_one({'_id': ObjectId(account_id)})
    return render_template('pm_show.html', account=account)

# code for editing account
@app.route('/accounts/<account_id>', methods=['POST'])
def account_update(account_id):
    updated_account = {
        'platform': request.form.get('platform'),
        'id': request.form.get('id'),
        'password': request.form.get('password'),
        'url': request.form.get('url')
    }
    accounts.update_one(
        {'_id': ObjectId(account_id)},
        {'$set': updated_account})
    return redirect(url_for('account_show', account_id=account_id))

# edit route
@app.route('/accounts/<account_id>/edit')
def account_edit(account_id):
    account = accounts.find_one({'_id': ObjectId(account_id)})
    return render_template('pm_edit.html', account=account, title='Edit Account')

# delete route
@app.route('/accounts/<account_id>/delete', methods=['POST'])
def account_delete(account_id):
    accounts.delete_one({'_id': ObjectId(account_id)})
    return redirect(url_for('pm_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))