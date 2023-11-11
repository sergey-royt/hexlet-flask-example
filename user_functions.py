import json


def validator(user):
    errors = {}
    if len(user.get('username', 's')) < 4:
        errors['username'] = 'Nickname must be grater than 4 characters'
    if not user.get('e-mail'):
        errors['e-mail'] = "Can't be blank"
    return errors


def edit_validator(user):
    errors = {}
    username = user.get('username')

    if username and len(username) < 4:
        errors['username'] = 'Nickname must be grater than 4 characters'

    return errors


def edit_user(repo, data, id):
    if data.get('username'):
        repo[id]['username'] = data['username']

    if data.get('e-mail'):
        repo[id]['e-mail'] = data['e-mail']


def create(repo, user):
    id = len(repo) + 1
    repo[id] = user
    return id

def log_in(repo, e_mail):
    for user in repo:
        if repo[user]['e-mail'] == e_mail:
            return True
        return False
