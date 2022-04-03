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
    
@app.route('/')
def index() :
    repos_path = os.getcwd() + '/app/static/repo_list.json'
    with open(repos_path, 'r') as f :
        repos = json.loads(f.read())
        total = len(repos) # the number of repositories
        
        # only first 12 repositories will be printed
        repos_12 = []
        for i in range(12) : # append 12 repositories
            repos_12.append(repos['repo_' + str(i)])
        repos_12 = { i: repos_12[i] for i in range(len(repos_12))} # list -> dict
    return render_template('index.html', total=total, repos=repos_12)
    
@app.route('/data')
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('data.html', signin=ret)