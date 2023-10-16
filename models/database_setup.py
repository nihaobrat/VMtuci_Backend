from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# Таблица для отношения "многие ко многим" между Пользователями и Подписчиками
followers_table = Table('followers', Base.metadata,
                        Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
                        Column('followee_id', Integer, ForeignKey('users.id'), primary_key=True)
                        )

# Таблица для лайков на постах
post_likes_table = Table('post_likes', Base.metadata,
                         Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                         Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True)
                         )

# Таблица для лайков на комментариях
comment_likes_table = Table('comment_likes', Base.metadata,
                            Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                            Column('comment_id', Integer, ForeignKey('comments.id'), primary_key=True)
                            )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password_hash = Column(String)

    # Связи
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    followed = relationship('User', secondary=followers_table, primaryjoin=id == followers_table.c.follower_id,
                            secondaryjoin=id == followers_table.c.followee_id, back_populates='followers')
    followers = relationship('User', secondary=followers_table, primaryjoin=id == followers_table.c.followee_id,
                             secondaryjoin=id == followers_table.c.follower_id, back_populates='followed')
    liked_posts = relationship('Post', secondary=post_likes_table, back_populates='likers')
    liked_comments = relationship('Comment', secondary=comment_likes_table, back_populates='likers')


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Связи
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likers = relationship('User', secondary=post_likes_table, back_populates='liked_posts')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Связи
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
    likers = relationship('User', secondary=comment_likes_table, back_populates='liked_comments')

# Этот код не будет выполнять никаких действий, пока не будет создан engine
# и не будет вызван метод create_all для Base.
# engine = create_engine('postgresql://username:password@localhost/db_name')
# Base.metadata.create_all(engine)
