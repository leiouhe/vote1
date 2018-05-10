from flask import Flask, request, render_template, redirect, url_for, session
from vote1.models import Item

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config.from_object(__name__)

#config
app.config.update(dict(
    DATAPATH = 'localhost',
    DATABASE = 'votes',
    ROOTNAME = 'admin1',
    ROOTPASS = '123456',
    DEBUG = True,
    SECRET_KEY = 'development key'
))

#override config from an environment variable,if none: silent
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + app.config['ROOTNAME'] + ':' + app.config['ROOTPASS'] + '@' + app.config['DATAPATH'] + '/' + app.config['DATABASE']
#比较 mysql-python作为DBAPI

# engine = create_engine('mysql+mysqlconnector://admin1:123456@localhost/votes', convert_unicode=True)
engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True)

#以下模式，在整个程序运行的过程当中，只存在唯一的一个session对象
#比较下其他模式
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)


#functions
#票数+1
def vote_plus(vote_id):
    vote_item = Item.query.filter_by(id=vote_id).first()
    vote_item.votes += 1
    db_session.commit()

#增加选项
def add_item(title):
    item = Item(title,0)
    db_session.add(item)
    db_session.commit()

# --提交要加个前端验证，如果一个都没选，提示
# 刷新自动提交的问题修正
@app.route('/',methods=['GET','POST'])
def vote():
    if request.method == 'POST':
        vote_id = int(request.form['vote'])
        vote_plus(vote_id)
    items = Item.query.all()
    url = url_for('create_item')
    request_list = dir(request)
    session_list = dir(session)
    return render_template('index.html', items=items, create_item_url=url,request_list=request_list, session_list=session_list)


@app.route('/createitem', methods=['GET','POST'])
def create_item():
    if request.method == 'POST':
        title = request.form['vote_item']
        add_item(title)
        return redirect(url_for('vote'))
    else:
        return render_template('create.html')



# 数据库新增字段，迁移

#修改自己的选择，提交
# @app.route()
# def change_vote():

# 用户认证



#发起新的票选，可选重新邀请重投等


#管理员，删除修改所有等


#automatically remove database sessions at the end of the request or when the application shuts down:
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
