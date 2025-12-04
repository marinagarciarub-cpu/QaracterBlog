from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/qaracter_blog')
client = MongoClient(MONGO_URI)
db = client['qaracter_blog']

# Colecciones
users_collection = db['users']
posts_collection = db['posts']

# Crear índices únicos
users_collection.create_index('username', unique=True)


class User:
    def __init__(self, username, password, _id=None):
        self.username = username
        self.password = generate_password_hash(password)
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()
    
    def save(self):
        user_dict = {
            '_id': self._id,
            'username': self.username,
            'password': self.password,
            'created_at': self.created_at
        }
        result = users_collection.insert_one(user_dict)
        self._id = result.inserted_id
        return self
    
    def to_dict(self, include_password=False):
        data = {
            '_id': str(self._id),
            'username': self.username,
            'created_at': self.created_at.isoformat()
        }
        if include_password:
            data['password'] = self.password
        return data
    
    @staticmethod
    def find_by_id(user_id):
        try:
            user_data = users_collection.find_one({'_id': ObjectId(user_id)})
            if user_data:
                user = User(user_data['username'], '', _id=user_data['_id'])
                user.password = user_data['password']
                user.created_at = user_data.get('created_at', datetime.utcnow())
                return user
        except:
            pass
        return None
    
    @staticmethod
    def find_by_username(username):
        user_data = users_collection.find_one({'username': username})
        if user_data:
            user = User(user_data['username'], '', _id=user_data['_id'])
            user.password = user_data['password']
            user.created_at = user_data.get('created_at', datetime.utcnow())
            return user
        return None


class Post:
    def __init__(self, title, content, user_id, _id=None):
        self.title = title
        self.content = content
        self.user_id = user_id
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        post_dict = {
            '_id': self._id,
            'title': self.title,
            'content': self.content,
            'author_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        result = posts_collection.insert_one(post_dict)
        self._id = result.inserted_id
        return self
    
    def to_dict(self, include_id=False):
        user = User.find_by_id(self.user_id)
        author_name = user.username if user else 'Unknown'
        
        data = {
            'title': self.title,
            'content': self.content,
            'author_id': self.user_id,
            'author': author_name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_id:
            data['_id'] = self._id
        else:
            data['id'] = str(self._id)
        return data
    
    @staticmethod
    def find_by_id(post_id):
        try:
            post_data = posts_collection.find_one({'_id': ObjectId(post_id)})
            if post_data:
                post = Post(post_data['title'], post_data['content'], post_data['author_id'], _id=post_data['_id'])
                post.created_at = post_data.get('created_at', datetime.utcnow())
                post.updated_at = post_data.get('updated_at', datetime.utcnow())
                return post
        except:
            pass
        return None
    
    @staticmethod
    def find_by_user_id(user_id):
        posts = []
        try:
            posts_data = posts_collection.find({'author_id': user_id}).sort('created_at', -1)
            for post_data in posts_data:
                post = Post(post_data['title'], post_data['content'], post_data['author_id'], _id=post_data['_id'])
                post.created_at = post_data.get('created_at', datetime.utcnow())
                post.updated_at = post_data.get('updated_at', datetime.utcnow())
                posts.append(post)
        except:
            pass
        return posts
    
    @staticmethod
    def find_all():
        posts = []
        try:
            posts_data = posts_collection.find().sort('created_at', -1)
            for post_data in posts_data:
                post = Post(post_data['title'], post_data['content'], post_data['author_id'], _id=post_data['_id'])
                post.created_at = post_data.get('created_at', datetime.utcnow())
                post.updated_at = post_data.get('updated_at', datetime.utcnow())
                posts.append(post)
        except:
            pass
        return posts
    
    @staticmethod
    def delete_by_id(post_id):
        try:
            posts_collection.delete_one({'_id': ObjectId(post_id)})
            return True
        except:
            return False
