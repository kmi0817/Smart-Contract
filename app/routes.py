from select import select
from app import app
from flask import render_template, session, request, send_file
import json
import os.path
import re # sortf
import zipfile # zip 객체
from collections import defaultdict # search

directory_path = os.getcwd() + '/app/static/data/'

data = defaultdict(list) # for search

@app.route('/')
def index() :
    # GET 가져오기
    search = request.args.get('search')
    sortedBy = request.args.get('sortedBy')

    # 검색어 입력X
    if search == None :
        # sorting parameter별 가져올 json 파일 처리
        if sortedBy == None or sortedBy == 'created_at': # 디폴트: created_by
            repo_name = create_json_sorted_by_created_at(directory_path + 'repo_list.json')
            sorting_type = 'Newly Created'
        elif sortedBy == 'star' : # most stars
            repo_name = create_json_sorted_by_star(directory_path + 'repo_list_time_sort.json')
            sorting_type = 'Most Stars'
        elif sortedBy == 'name' : # name ascending
            repo_name = create_json_sorted_by_name(directory_path + 'repo_list_time_sort.json')
            sorting_type = 'Names Ascending'

    # 검색어 입력O
    else :
        search = search.lower() # 소문자로 변경
        repo_searched = create_json_searched(directory_path + 'repo_list_time_sort.json', search)
        if sortedBy == None or sortedBy == 'created_at': # 디폴트: created_by
            repo_name = create_json_sorted_by_created_at(directory_path + repo_searched)
            sorting_type = 'Newly Created'
        elif sortedBy == 'star' : # 검색 결과에서 most stars 정렬
            repo_name = create_json_sorted_by_star(directory_path + repo_searched)
            sorting_type = 'Most Stars'
        elif sortedBy == 'name' : # 검색 결과에서 name ascending 정렬
            repo_name = create_json_sorted_by_name(directory_path + repo_searched)
            sorting_type = 'Names Ascending'

    # json 파일 경로 구성
    repos_path = directory_path + repo_name

    # json 파일 내 12개의 repositories 정보만 가져옴
    with open(repos_path, 'r') as f :
        repos = json.loads(f.read())
        total = len(repos) # the number of repositories
        
        repos_printed = [] # 먼저 출력될 repository 담는 리스트
        if total >= 12 : # repository가 12개 이상 존재할 때
            for i in range(12) : # 12개의 repository를 append
                repos_printed.append(repos['repo_' + str(i)])
        else : # repository가 12개 미만으로 존재할 때
            for i in range(total) : # 모든 repository를 append
                repos_printed.append(repos['repo_' + str(i)])
        
        repos_printed = { i: repos_printed[i] for i in range(len(repos_printed))} # list -> dict
        
    return render_template('index.html', total=total, repos=repos_printed, repo_name=repo_name, sorting_type=sorting_type, search=search)

@app.route('/download-current-repositories', methods=['POST'])
def download() :
    repo_name = request.form['repo_name'] # 다운로드할 JSON 데이터 제목 가져오기
    repos_path = directory_path + repo_name # 경로와 파일 제목 합치기
    return send_file(repos_path, as_attachment=True)

@app.route('/download-selected-repositories', methods=['POST'])
def download_selected_repositories() :
    selected_repos = request.get_json(force=True) # POST로 보낸 데이터 받기

    changed_cwd = os.chdir(directory_path + 'zips/') # zips 디렉터리로 current working directory 경로 변경
    zips_list = os.listdir(changed_cwd) # zips 디렉터리 내 모든 파일 리스트 가져오기

    selected_zips = [ zip for zip in zips_list if zip in selected_repos.values() ] # 선택된 레포지터리의 zip 파일 리스트

    with zipfile.ZipFile('../selected_repos.zip', 'w') as z : # zip 파일 write 모드
        for zip in selected_zips :
            z.write(zip) # 선택된 레포지터리의 zip 파일들을 selected_repos.zip 파일에 write
        z.close()

    return {'message': "OK"}

@app.route('/webix') # backup용 (무시)
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('webix.html', signin=ret)

# 검색 함수
def create_json_searched(original, word) :
    with open(original, "r") as f:
        repo_list = json.load(f)

    # repo_list 딕셔너리의 key와 value를 순회하면서 value['name']에 검색어(word)가 포함되어 있다면  searched_list 추가하기
        # key 값이 순차적으로 증가하지 않음 ex) { 'repo_0': {  ... }, 'repo_1891': { ... } } 
    searched_list = {
        key : value for key, value in repo_list.items() if word in value['name'].lower()
    }

    # repo_list의 value를 순회하면서 refined_searched_list에 추가하기
        # refined_searched_list의 key는 순차적으로 증가함
    refined_searched_list = {
        f'repo_{i}' : value for i, value in enumerate(searched_list.values())
    }

    file_name = 'repo_list_search.json'
    file_path = directory_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(refined_searched_list, file, indent="\t")

    return file_name

# Newly Created 정렬
def create_json_sorted_by_created_at(original) :
    with open(original,"r") as f:
        repo_list = json.load(f)

    sorted_list = sorted(repo_list.values(), key=lambda x : x['create_time'], reverse=True) # create_time 내림차순 정렬
        # 타입이 리스트임 ex) [ { "name": "pasDamola/smart_contract_repo", ... }, { "name": "matiasdamelio/smart_contract_bootcamp" }, ... ]

    refined_sorted_list = { f'repo_{i}' : value for i, value in enumerate(sorted_list) } # 딕셔너리로 생성

    #이름 정렬 json파일은 따로 저장
    file_name = 'repo_list_time_sort.json'
    file_path = directory_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(refined_sorted_list, file, indent="\t")
    return file_name

def create_json_sorted_by_name(original) :
    with open(original,"r") as f:
        j_file = json.load(f)
    # print(json.dumps(j_file, sort_keys=False, indent=4))

    key1_list = list(j_file.keys()) #첫번째 key
    value1_list = list(j_file.values())
    key2_list = list(value1_list[0].keys()) #두번째 key
    # print(key2_list)

    #정렬할 내용: 이름과 star
    name_list = dict()
    star_list = dict()
    l =range(len(j_file)) #json 파일의 개수



    #이름 순서대로 정렬
    for i in l: #key1과 value2의 내용을 연결
        key1_name = 'repo_' + str(i)
        name_list[key1_name] = j_file[key1_name]['name']
    # print(json.dumps(updated_list, sort_keys=False, indent=4))

    #이름 순서대로 정렬해줌
    name_sort = dict(sorted(name_list.items(), key=lambda x :x[1]))
    # print(json.dumps(name_sort, sort_keys=False, indent=4))

    #이름 순서대로 정렬된 것을 다시 json에 저장
    tmp_name = {}
    k_name=list(name_sort.keys())
    for a in l: # tmp의 key에 새로 정렬한 key의 순서대로 들어감
        new_key_name = k_name[a] #새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 지정해줌
        item = dict(j_file[new_key_name].items()) #key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(a):item}#tmp딕셔너리에 저장
        tmp_name.update(f)
    # print(tmp_name)

    #이름 정렬 json파일은 따로 저장
    file_name = 'repo_list_name_sort.json'
    file_path = directory_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tmp_name, file, indent="\t")
    return file_name

# Most Stars 정렬
def create_json_sorted_by_star(original) :
    with open(original,"r") as f:
        repo_list = json.load(f)

    repos_have_star = [] # star 필드가 0 ~ 9인 value 담는 리스트
    repos_dont_have_star = [] # star 필드가 null이거나 이상한 값인 value 담는 리스트

    for value in repo_list.values() :  # 모든 value를 순회하며 star 필드 값에 따라 서로 다른 리스트에 담기
        if value['star'] is not None :
            if re.match('[^0-9]', value['star']) :
                repos_dont_have_star.append(value) # 이상한 값
            else :
                repos_have_star.append(value) # 0 ~ 9
        else :
            repos_dont_have_star.append(value) # null

    sorted_list = sorted(repos_have_star, key=lambda x : int(x['star']), reverse=True) # star 내림차순 정렬
    sorted_list.extend(repos_dont_have_star) # 두 리스트 합치기

    refined_sorted_list = { f'repo_{i}' : value for i, value in enumerate(sorted_list) } # 딕셔너리 생성

    #정렬 json파일은 따로 저장
    file_name = 'repo_list_star_sort.json'
    file_path = directory_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(refined_sorted_list, file, indent="\t")
    return file_name