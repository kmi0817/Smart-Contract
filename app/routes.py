from app import app
from flask import render_template, session
import json
import pymongo
import os.path

try :
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMs = 1000
    )
    db = mongo.smart_contract
    mongo.server_info() # trigger exception if cannot connect to db
except :
    print("** error - cannot connect to DB")
    
@app.route('/index')
def index() :
    repos_path = os.getcwd() + '/app/static/repo_test.json'
    with open(repos_path, 'r') as f :
        repos = json.loads(f.read())
    return render_template('index.html', repos=repos)
    
@app.route('/')
def home() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('home.html', signin=ret)

@app.route('/data')
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('data.html', signin=ret)