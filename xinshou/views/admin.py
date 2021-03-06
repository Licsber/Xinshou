import json
from json import JSONDecodeError

import requests
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_httpauth import HTTPBasicAuth

mod = Blueprint('admin', __name__)
auth = HTTPBasicAuth()


@auth.get_password
def get_passwd(username):
    if username == 'licsber':
        return current_app.config['ADMIN_PASSWD']


@mod.route('/')
@auth.login_required
def index():
    if len(request.args) != 0 and request.args['ak'] == 'licsber':
        return render_template('admin-manager.html')
    return 'Hello from Licsber.'


@mod.route('/settings')
@auth.login_required
def settings():
    msg = request.args['msg'] if 'msg' in request.args else ''
    return render_template('admin-settings.html', msg=msg,
                           input_json=current_app.config['DEFAULT_MENU'])


@mod.route('/face-manager')
@auth.login_required
def face_manager():
    all = current_app.auth.get_all()
    return render_template('face-manager.html', all=all)


@mod.route('/user-info', methods=['POST'])
def get_user_info():
    params = {
        'access_token': current_app.admin.get_access_token(),
        'openid': request.form['input']
    }
    res = requests.get(current_app.config['API_USER_INFO'], params=params)
    return redirect(url_for('admin.settings', msg=res.content))


@mod.route('/delete-all-menu')
@auth.login_required
def delete_all_menu():
    params = {'access_token': current_app.admin.get_access_token()}
    res = requests.get(current_app.config['API_MENU_DELETE'], params=params)
    return redirect(url_for('admin.settings', msg=res.content))


@mod.route('/get-all-menu')
@auth.login_required
def get_all_menu():
    params = {'access_token': current_app.admin.get_access_token()}
    res = requests.get(current_app.config['API_MENU_INFO'], params=params)
    return redirect(url_for('admin.settings', msg=res.content))


@mod.route('/set-all-menu', methods=['POST'])
@auth.login_required
def set_all_menu():
    j = request.form['json']
    try:
        j = json.loads(j)
    except JSONDecodeError as e:
        return redirect(url_for('admin.settings', msg='JSON格式错误, 示例：{"button":[{type,name,url}]}.'))
    j = json.dumps(j, ensure_ascii=False).encode('utf-8')
    params = {'access_token': current_app.admin.get_access_token()}
    res = requests.post(current_app.config['API_MENU_CREATE'], params=params, data=j)
    return redirect(url_for('admin.settings', msg=res.content))
