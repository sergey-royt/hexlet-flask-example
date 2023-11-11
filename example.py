from flask import Flask, session, render_template, request, redirect, url_for, flash, get_flashed_messages, make_response
import json
import user_functions


app = Flask(__name__)

app.secret_key = "secret_key"


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.route('/courses/<id>')
def courses(id):
    return f'Course id: {id}'


@app.route('/users/<id>')
def get_user(id):
    users = json.loads(request.cookies.get('users', json.dumps({})))
    user = users.get(id)
    if user:
        return render_template(
                'users/show.html',
                id=id,
                user=user
            )
    else:
        return 'User not found', 404


@app.route('/users/')
def list_users():
    messages = get_flashed_messages(with_categories=True)
    auth = session.get('login')
    users = json.loads(request.cookies.get('users', json.dumps({})))
    term = request.args.get('term') or ''
    filtered_users = {k: v for k, v in users.items() if term in v['username']}
    response = make_response(render_template('users/index.html', users=filtered_users, search=term, messages=messages, auth=auth))
    response.set_cookie('users', json.dumps(users))
    return response


@app.route('/users/new/')
def page():
    messages = get_flashed_messages(with_categories=True)
    errors = {}
    return render_template('users/new.html', errors=errors, messages=messages)


@app.post('/users')
def create_user():
    temp_repo = json.loads(request.cookies.get('users', json.dumps({})))
    data = request.form.to_dict()
    errors = user_functions.validator(data)
    if errors:
        flash('Error while creating user', 'error')
        return render_template('users/new.html', errors=errors, messages=get_flashed_messages(with_categories=True))
    user_functions.create(temp_repo, data)
    response = make_response(redirect(url_for('list_users'), code=302))
    response.set_cookie('users', json.dumps(temp_repo))
    flash('User was added successfully', 'success')
    return response


@app.get('/users/<id>/edit')
def edit_page(id):
    users = json.loads(request.cookies.get('users', json.dumps({})))
    user = users.get(id)
    errors = {}

    return render_template('users/edit.html', user=user, errors=errors, id=id)


@app.post('/users/<id>/patch')
def update_user(id):
    users = json.loads(request.cookies.get('users', json.dumps({})))
    data = request.form.to_dict()
    errors = user_functions.edit_validator(data)

    if errors:
        return render_template(
            'users/edit.html',
            user=data,
            errors=errors,
            id=id
        ), 422

    user_functions.edit_user(users, data, id)
    response = make_response(redirect(url_for('list_users')))
    response.set_cookie('users', json.dumps(users))
    flash('User has been updated', 'success')
    return response


@app.post('/users/<id>/delete')
def delete_user(id):
    repo = json.loads(request.cookies.get('users', json.dumps({})))
    del repo[id]
    response = make_response(redirect(url_for('list_users')))
    response.set_cookie('users', json.dumps(repo))
    flash('User has been deleted', 'success')
    return response


@app.get('/login')
def log_in_page():
    return render_template('users/login.html')

@app.post('/login')
def log_in():
    repo = json.loads(request.cookies.get('users', json.dumps({})))
    e_mail = request.form.get('e-mail')
    session['login'] = user_functions.log_in(repo, e_mail)
    return redirect(url_for('list_users'))

@app.post('/logout')
def log_out():
    del session['login']
    return redirect(url_for('list_users'))
