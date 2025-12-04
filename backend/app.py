from flask import Flask, request, jsonify
from flask_cors import CORS
from models import User, Post, users_collection, posts_collection
from datetime import datetime
from werkzeug.security import check_password_hash
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)


# ==================== USUARIOS ====================

@app.route('/api/users', methods=['POST'])
def create_user():
    """Crear un nuevo usuario"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username y password son requeridos'}), 400
    
    if User.find_by_username(data['username']):
        return jsonify({'message': 'Username ya existe'}), 409
    
    user = User(data['username'], data['password'])
    user.save()
    
    return jsonify({'message': 'Usuario creado', 'user': user.to_dict()}), 201


@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Obtener información de un usuario"""
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    return jsonify(user.to_dict()), 200


# ==================== POSTS ====================

@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    """Obtener todos los posts"""
    posts = Post.find_all()
    return jsonify([post.to_dict() for post in posts]), 200


@app.route('/api/posts', methods=['POST'])
def create_post():
    """Crear un nuevo post"""
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content') or not data.get('user_id'):
        return jsonify({'message': 'title, content y user_id son requeridos'}), 400
    
    user = User.find_by_id(data['user_id'])
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    post = Post(data['title'], data['content'], data['user_id'])
    post.save()
    
    return jsonify({'message': 'Post creado', 'post': post.to_dict()}), 201


@app.route('/api/posts/<post_id>', methods=['GET'])
def get_post(post_id):
    """Obtener un post específico"""
    post = Post.find_by_id(post_id)
    
    if not post:
        return jsonify({'message': 'Post no encontrado'}), 404
    
    return jsonify(post.to_dict()), 200


@app.route('/api/posts/<post_id>', methods=['PUT'])
def update_post(post_id):
    """Actualizar un post"""
    post = Post.find_by_id(post_id)
    
    if not post:
        return jsonify({'message': 'Post no encontrado'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        post.title = data['title']
    
    if 'content' in data:
        post.content = data['content']
    
    post.updated_at = datetime.utcnow()
    post.save()
    
    return jsonify({'message': 'Post actualizado', 'post': post.to_dict()}), 200


@app.route('/api/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Eliminar un post"""
    post = Post.find_by_id(post_id)
    
    if not post:
        return jsonify({'message': 'Post no encontrado'}), 404
    
    Post.delete_by_id(post_id)
    
    return jsonify({'message': 'Post eliminado'}), 200


@app.route('/api/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Obtener todos los posts de un usuario"""
    user = User.find_by_id(user_id)
    
    if not user:
        return jsonify({'message': 'Usuario no encontrado'}), 404
    
    posts = Post.find_by_user_id(user_id)
    
    return jsonify([post.to_dict() for post in posts]), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)