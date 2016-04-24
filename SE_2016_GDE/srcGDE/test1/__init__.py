from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import json
from flask.ext.jsonpify import jsonify

badge = Flask(__name__)
badge.config.from_object('test1.config')
db = SQLAlchemy(badge)
from test1 import models
from test1.models import *
test1 = Blueprint('test1', 'test1')

#========= The above part will be more or less the same for all GDE =======#

#========================= Non-route functions ============================#

def add_user(username):
    me = User(username)
    db.session.add(me)
    db.session.commit()
    return

def find_user_force(username):
    user = User.query.filter_by(nickname=username).first()
    if user is None:
        add_user(username)
        user = User.query.filter_by(nickname=username).first()
    return user

def find_badge(name):
    badge = Badge.query.filter_by(name=name).first()
    return badge

def delete_all_users(username):
    users = User.query.all()
    for user in users:
        db.session.delete(user)
    db.session.commit()

#========================= Routes are defined below =======================#

@test1.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'test1 module'

@test1.route('/users', methods=["GET"])
def show_all_users():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'name': user.nickname
        })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@test1.route('/user/<page>', methods=["GET"])
def show_user(page):
    user = User.query.filter_by(nickname=page).first()
    badge_ids = UserBadge.query.filter_by(user_id=user.id)
    test1 = []
    for b in badge_ids:
        badge = Badge.query.filter_by(id=b.badge_id).first()
        test1.append(badge.to_dict())
    data = ({
        'id': user.id,
        'name': user.nickname,
        'test1': test1
    })
    return jsonify({
        'success': True,
        'message': 'User exist',
        'data': data
    })

@test1.route('/create', methods=["POST"])
def create_badge():
    try:
        badge = Badge(request.form['name'], request.form['description'], request.form['image_name'])
        db.session.add(badge)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Badge added successfully'
    })

@test1.route('/list', methods=["GET"])
def show_all_test1():
    test1 = Badge.query.all()
    data = []
    for badge in test1:
        data.append(badge.to_dict())
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@test1.route('/addnotify', methods=["GET"])
def create_notification():
    notify = Notifications(user=request.args.get('user'), target=request.args.get('target'), message=request.args.get('message'))
    find_user_force(request.args.get('user'))
    
    find_user_force(request.args.get('target'))
    db.session.add(notify)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Not awarded successfully'
    })

@test1.route('/notifications', methods=["GET"])
def show_all_notifications():
    users = Notifications.query.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'user': user.user,
            'target': user.target,
            'message': user.message
        })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@test1.route('/notifications_user', methods=["GET"])
def show_all_notificationsbyuser():
    users = Notifications.query.filter_by(user=request.args.get('user'))
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'user': user.user,
            'target': user.target,
            'message': user.message
        })
    return jsonify({
        'success': True,
        'message': '',
        'data': data
    })

@test1.route('/award', methods=["POST"])
def create_badge_user_mapping():
    try:
        user = find_user_force(request.form['username'])
        badge = find_badge(request.form['badge'])
        existing = UserBadge.query.filter_by(user_id=user.id, badge_id=badge.id).all()
        if len(existing) > 0:
            return jsonify({
                'success': False,
                'message': 'User already has this badge'
            })
        mapping = UserBadge(user, badge)
        db.session.add(mapping)
        db.session.commit()
    except:
        return jsonify({
            'success': False,
            'message': 'Something went wrong :('
        })
    return jsonify({
        'success': True,
        'message': 'Badge awarded successfully'
    })

@test1.route('/static/<page>', methods=["GET"])
def send_static(page):
    return send_from_directory('test1/static', page)