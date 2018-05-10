from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#比较 mysql-python作为DBAPI

engine = create_engine('mysql+mysqlconnector://admin1:123456@localhost/votes', convert_unicode=True)

#以下模式，在整个程序运行的过程当中，只存在唯一的一个session对象
#比较下其他模式
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    Base.metadata.create_all(bind=engine)