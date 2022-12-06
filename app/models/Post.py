from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
from sqlalchemy.orm import relationship, column_property

class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  user = relationship('User')

  # associate posts and comments so that a query for a post also returns information about any comments on it
  # the cascade='all,delete' statement means that if a post is deleted from the database, it also deletes all its associated comments
  comments = relationship('Comment', cascade='all,delete')
  
  votes = relationship('Vote', cascade='all,delete')
 
  # creates dynamic column that updates the vote count
  vote_count = column_property(
    select([func.count(Vote.id)]).where(Vote.post_id == id)
  )