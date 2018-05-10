from sqlalchemy import Column, Integer, String
from vote1.database import Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    votes = Column(Integer)

    def __init__(self, title=None, votes=None):
        self.title = title
        self.votes = votes

    def __repr__(self):
        return '<Title: %r, votes: %r>' % (self.title,self.votes)