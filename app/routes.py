from app import app
from flask import render_template, session, request
import json
import os.path
import re # sortf
from collections import defaultdict # search

direcotry_path = os.getcwd() + '/app/static/'

data = defaultdict(list) # for search

@app.route('/')
def index() :
    # GET 가져오기
    search = request.args.get('search')
    sortedBy = request.args.get('sortedBy')
    print("search:", search)
    # 검색어 입력X
    if search == None :
        # sorting parameter별 가져올 json 파일 처리
        if sortedBy == None or sortedBy == 'created_at': # 디폴트: created_by
            repo_name = create_json_sorted_by_created_at(direcotry_path + 'repo_list.json')
            sorting_type = 'Newly Created'
        elif sortedBy == 'star' : # most stars
            repo_name = create_json_sorted_by_star(direcotry_path + 'repo_list_time_sort.json')
            sorting_type = 'Most Stars'
        elif sortedBy == 'name' : # name ascending
            repo_name = create_json_sorted_by_name(direcotry_path + 'repo_list_time_sort.json')
            sorting_type = 'Names Ascending'

    # 검색어 입력O
    else :
        print("In index, 검색어는 ", search)
        repo_searched = create_json_searched(direcotry_path + 'repo_list_time_sort.json', search)
        if sortedBy == None or sortedBy == 'created_at': # 디폴트: created_by
            repo_name = create_json_sorted_by_created_at(direcotry_path + repo_searched)
            sorting_type = 'Newly Created'
        elif sortedBy == 'star' : # 검색 결과에서 most stars 정렬
            repo_name = create_json_sorted_by_star(direcotry_path + repo_searched)
            sorting_type = 'Most Stars'
        elif sortedBy == 'name' : # 검색 결과에서 name ascending 정렬
            repo_name = create_json_sorted_by_name(direcotry_path + repo_searched)
            sorting_type = 'Names Ascending'

    # json 파일 경로 구성
    repos_path = direcotry_path + repo_name

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
        
    return render_template('index.html', total=total, repos=repos_printed, repo_name=repo_name, sorting_type=sorting_type)
    
@app.route('/webix') # backup용 (무시)
def data() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('webix.html', signin=ret)

# 검색 함수 (연구실 선배가 작성한 알고리즘)
def create_json_searched(original, word) :
    with open(original, "r") as f:
        j_file = json.load(f)
    key1_list = list(j_file.keys())  # 첫번째 key
    value1_list = list(j_file.values())
    key2_list = list(value1_list[0])  # 두번째 key
    l = range(len(j_file))  # json 파일의 개수

    find_list = dict()  # 단어를 포함하고 있는 문자열들만 저장하는 딕셔너리
    for i in l:  # key1과 value2의 내용을 연결, 새로운 딕셔너리 파일 생성
        value2 = j_file[key1_list[i]]['name']  # 찾아낸 value값만 따로 만들어둠
        find_word = value2.find(word)  # 입력받은 문자 찾기
        if find_word != -1:  # 문자를 포함하지 않는 경우 -1을 반환하므로 이보다 큰 수를 찾기
            find_list[key1_list[i]] = value2

    ll = range(len(find_list))
    tmp_search = {}
    k_search = list(find_list.keys())  # 찾은 값의 key값
    for a in ll:
        new_key_search = k_search[a]  # 새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 그대로 가져옴
        item = dict(j_file[new_key_search].items())  # key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(a): item}  # tmp딕셔너리에 저장
        tmp_search.update(f)

    file_name = 'repo_list_search.json'
    file_path = direcotry_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tmp_search, file, indent="\t")
    print("In search function!!!!")
    return file_name

# 정렬 함수 (연구실 선배가 작성한 알고리즘)
def create_json_sorted_by_created_at(original) :
    with open(original,"r") as f:
        j_file = json.load(f)

    #key와 value를 분리
    key1_list = list(j_file.keys()) #첫번째 key
    value1_list = list(j_file.values())
    key2_list = list(value1_list[0].keys()) #두번째 key
    # print(key2_list)

    #정렬을 위해 두번째 key만 분류
    time_list = dict()

    l =range(len(j_file)) #json 파일의 개수
    for i in l: #key1과 value2의 내용을 연결
        key1_name = 'repo_' + str(i)
        time_list[key1_name] = j_file[key1_name]['create_time']
    # print(json.dumps(updated_list, sort_keys=False, indent=4))

    #날짜 순서대로 정렬해줌
    time_sort = dict(sorted(time_list.items(), key=lambda x :x[1], reverse = True))

    #시간 순서대로 정렬된 것을 다신 json에 저장
    tmp_time = {}
    k_time=list(time_sort.keys())
    for a in l: # tmp의 key에 새로 정렬한 key의 순서대로 들어감
        new_key_time = k_time[a] #새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 지정해줌
        item = dict(j_file[new_key_time].items()) #key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(a):item}#tmp딕셔너리에 저장
        tmp_time.update(f)
    # print(tmp_time)

    #이름 정렬 json파일은 따로 저장
    file_name = 'repo_list_time_sort.json'
    file_path = direcotry_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tmp_time, file, indent="\t")
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
    file_path = direcotry_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tmp_name, file, indent="\t")
    return file_name

def create_json_sorted_by_star(original) :
    with open(original,"r") as f:
        j_file = json.load(f)
    # print(json.dumps(j_file, sort_keys=False, indent=4))

    key1_list = list(j_file.keys()) #첫번째 key
    value1_list = list(j_file.values())
    key2_list = list(value1_list[0].keys()) #두번째 key
    # print(key2_list)

    #정렬할 내용: 이름과 star
    l =range(len(j_file)) #json 파일의 개수

    #별의 개수대로 정렬
    star_list_null = dict()
    star_list_not_null_alpha = dict()
    star_list_not_null_num = dict()
    for i in l: #key1과 value2의 내용을 연결
        key1_name = 'repo_' + str(i)
        if j_file[key1_name]['star'] is not None: #null이 아닌 경우
            if re.match('[^0-9]', j_file[key1_name]['star']):
                star_list_not_null_alpha[key1_name] = j_file[key1_name]
            else:
                star_list_not_null_num[key1_name] = j_file[key1_name]
        else:
            star_list_null[key1_name] = j_file[key1_name]
    # print(star_list_not_null)

    star_sort = dict(sorted(star_list_not_null_num.items(), key=lambda x :int(x[1]['star']), reverse=True))#star 순서대로 정렬

    #정렬이 된 star을 먼저 새로운 key값을 붙여줌
    tmp_star = {}
    k_star=list(star_sort.keys())
    ll =range(len(star_sort))
    for a in ll: # tmp의 key에 새로 정렬한 key의 순서대로 들어감
        new_key_star = k_star[a] #새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 지정해줌
        item = dict(j_file[new_key_star].items()) #key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(a):item}#tmp딕셔너리에 저장
        tmp_star.update(f)

    #star이 없는 dict에 새로운 key갑을 붙여줌
    tmp_star_null = {}
    k_star_null=list(star_list_null.keys())
    ll_null =range(len(star_list_null))
    for new_a in ll_null: # tmp의 key에 새로 정렬한 key의 순서대로 들어감
        lll=new_a+a+1
        new_key_star_null = k_star_null[new_a] #새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 지정해줌
        item = dict(j_file[new_key_star_null].items()) #key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(lll):item}#tmp딕셔너리에 저장
        tmp_star_null.update(f)

    # star 값이 이상한 dict에 새로운 key갑을 붙여줌
    tmp_star_alpha = {}
    k_star_alpha = list(star_list_not_null_alpha.keys())
    lll_null = range(len(star_list_not_null_alpha))
    for new_aa in lll_null:  # tmp의 key에 새로 정렬한 key의 순서대로 들어감
        alpha = new_aa + lll + 1
        new_key_star_alpha = k_star_alpha[new_aa]  # 새로 정렬된 딕셔너리 파일의 첫번쨰 key값을 지정해줌
        item = dict(j_file[new_key_star_alpha].items())  # key1에 해당하는 value값을 가지고 옴
        f = {"repo_{}".format(alpha): item}  # tmp딕셔너리에 저장
        tmp_star_alpha.update(f)

    tmp_star.update(tmp_star_null)  # star 두가지 정렬 합치기
    tmp_star.update(tmp_star_alpha)

    #정렬 json파일은 따로 저장
    file_name = 'repo_list_star_sort.json'
    file_path = direcotry_path + file_name
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(tmp_star, file, indent="\t")
    return file_name