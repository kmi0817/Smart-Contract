from app import app
from flask import render_template, redirect, url_for, session, request, jsonify
import pymongo

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
    return render_template('index.html')
    
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