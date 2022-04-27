from app import app
from flask import render_template, session, request
import json
import os.path

@app.route('/')
def index() :
    # sorting parameter별 가져올 json 파일 처리
    if request.args.get('sortedBy') == None : # 디폴트: created_by
        repo_name = 'repo_list.json'

    elif request.args.get('sortedBy') == 'star' : # most stars
        repo_name = 'repo_list.json'

    elif request.args.get('sortedBy') == 'name' : # name ascending
        repo_name = 'repo_list.json'

    # json 파일 경로 구성
    repos_path = os.getcwd() + f'/app/static/{repo_name}'

    # json 파일 내 12개의 repositories 정보만 가져옴
    with open(repos_path, 'r') as f :
        repos = json.loads(f.read())
        total = len(repos) # the number of repositories
        
        # only first 12 repositories will be printed
        repos_12 = []
        for i in range(12) : # append 12 repositories
            repos_12.append(repos['repo_' + str(i)])
        repos_12 = { i: repos_12[i] for i in range(len(repos_12))} # list -> dict
        
    return render_template('index.html', total=total, repos=repos_12, repo_name=repo_name)
    
@app.route('/webix')
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('webix.html', signin=ret)