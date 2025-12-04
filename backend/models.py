from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import os

MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/qaracter_blog')
client = MongoClient(MONGO_URI)
db = client['qaracter_blog']

# Colecciones
posts_collection = db['posts']


class Post:
    def __init__(self, title, content, author, _id=None):
        self.title = title
        self.content = content
        self.author = author
        self._id = _id or ObjectId()
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def save(self):
        post_dict = {
            '_id': self._id,
            'title': self.title,
            'content': self.content,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        result = posts_collection.insert_one(post_dict)
        self._id = result.inserted_id
        return self
    
    def to_dict(self, include_id=False):
        data = {
            'title': self.title,
            'content': self.content,
            'author': self.author,
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
                post = Post(post_data['title'], post_data['content'], post_data['author'], _id=post_data['_id'])
                post.created_at = post_data.get('created_at', datetime.utcnow())
                post.updated_at = post_data.get('updated_at', datetime.utcnow())
                return post
        except:
            pass
        return None
    
    @staticmethod
    def find_by_author(author):
        posts = []
        try:
            posts_data = posts_collection.find({'author': author}).sort('created_at', -1)
            for post_data in posts_data:
                post = Post(post_data['title'], post_data['content'], post_data['author'], _id=post_data['_id'])
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
                post = Post(post_data['title'], post_data['content'], post_data['author'], _id=post_data['_id'])
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
