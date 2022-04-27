from app import app
from flask import render_template, session, request
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
    # sorting parameter별 가져올 파일 처리
    if request.args.get('sortedBy') == None : # 디폴트: created_by
        repos_path = os.getcwd() + '/app/static/repo_list.json'

    elif request.args.get('sortedBy') == 'star' : # most stars
        repos_path = os.getcwd() + '/app/static/repo_list.json'

    elif request.args.get('sortedBy') == 'name' : # name ascending
        repos_path = os.getcwd() + '/app/static/repo_list.json'

    with open(repos_path, 'r') as f :
        repos = json.loads(f.read())
        total = len(repos) # the number of repositories
        
        # only first 12 repositories will be printed
        repos_12 = []
        for i in range(12) : # append 12 repositories
            repos_12.append(repos['repo_' + str(i)])
        repos_12 = { i: repos_12[i] for i in range(len(repos_12))} # list -> dict
    return render_template('index.html', total=total, repos=repos_12, repos_path=repos_path)
    
@app.route('/data')
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('data.html', signin=ret)