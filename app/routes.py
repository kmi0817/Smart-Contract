import re
from app import app
from app.models import Users, Postings, Comments
from flask import render_template, redirect, url_for, session, request, jsonify
import sys

@app.route('/')
def home() :
    ret = False
    if 'signin' in session :
        ret = True
    return render_template('home.html', signin=ret)

@app.route('/data')
def data() :
    return render_template('data.html')

@app.route('/board')
def board() :
    return render_template('board.html')

@app.route('/board/<int:id>')
def board_posting(id) :
    posting = Postings.query.filter_by(id=id).first()

    title = posting.title
    created_on = posting.created.strftime("%Y-%m-%d %H:%M")
    writer = posting.user_id
    content = posting.content

    return render_template('board_posting.html', posting_id=id, title=title, created_on=created_on, writer=writer, content=content)

@app.route('/board/write')
def board_write() :
    return render_template('write.html')

@app.route('/signin')
def signin() :
    if 'signin' in session :
        return redirect(url_for('home'))
    else :
        return render_template('signin.html')

@app.route('/signup')
def signup() :
    if 'signin' in session :
        return redirect(url_for('home'))
    else :
        return render_template('signup.html')

@app.route('/process-signout', methods=['POST'])
def process_signout() :
    session.pop('signin', None)
    return 'Sign Out'

@app.route('/process-signin', methods=['POST'])
def process_signin() :
    values = request.get_json(force=True) # dict 형태
    email = values['email']
    password = values['password']

    user = Users.query.filter_by(email=email).first() # DB에서 입력받은 email을 조건으로 레코드 찾기

    if user : # 만약 해당 이메일을 가진 레코드가 존재한다면,
        if user.email == email and user.password == password : # 이메일과 비밀번호가 모두 동일할 때
            ret = "OK"
            session['signin'] = email
        else : # 입력 내용이 DB 데이터와 불일치할 때
            ret = '<script>alert("Check your inputs"); history.go(-1);</script>'
    else : # 해당 이메일을 가진 레코드가 없을 때
        ret = '<script>alert("Check your inputs"); history.go(-1);</script>'

    return ret

@app.route('/process-signup', methods=['POST'])
def process_signup() :
    values = request.get_json(force=True) # dict
    email = values['email']
    password = values['password']

    # 입력 데이터를 DB에 저장하기 ...
    return values




# 데이터
@app.route('/database/postings')
def postings() :
    postings = Postings.query.all()

    output = []
    for post in postings :
        created_detail = post.created.strftime("%Y-%m-%d %H:%M")
        created_short = post.created.strftime("%m/%d")
        temp = {
            'id' : post.id,
            'user_id' : post.user_id,
            'title' : post.title,
            'created_detail' : created_detail,
            'created_short' : created_short,
            'content' : post.content
        }

        output.append(temp)
    output = jsonify(output)
    return output

@app.route('/database/postings/<id>')
def posting(id) :
    posting = Postings.query.filter_by(id=id).first()

    created_detail = posting.created.strftime("%Y-%m-%d %H:%M")
    created_short = posting.created.strftime("%m/%d")
    output = [{
        'id' : posting.id,
        'user_id' : posting.user_id,
        'title' : posting.title,
        'created_detail' : created_detail,
        'created_short' : created_short,
        'content' : posting.content
    }]
    output = jsonify(output)
    return output