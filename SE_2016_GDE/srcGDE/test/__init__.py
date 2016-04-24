from flask import Blueprint, render_template, abort, Flask, request, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
import json
from random import random
from flask.ext.jsonpify import jsonify

test = Blueprint('test', 'test')

#========= The above part will be more or less the same for all GDE =======#


#========================= Routes are defined below =======================#

@test.route('/', defaults={'page': 'index'})
def module_name(page):
    return 'Test module'

@test.route('/random', methods=["GET"])
def send_static():
    print '128 ('+str(int(random()*42+1))+').jpg'
    return send_from_directory('avatar/images', '128 ('+str(int(random()*42+1))+').jpg')