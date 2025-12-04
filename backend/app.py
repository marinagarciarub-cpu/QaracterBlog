from flask import Flask, request, jsonify
from flask_cors import CORS
from models import Post, posts_collection
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


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
    
    if not data or not data.get('title') or not data.get('content') or not data.get('author'):
        return jsonify({'message': 'title, content y author son requeridos'}), 400
    
    post = Post(data['title'], data['content'], data['author'])
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


@app.route('/api/posts/author/<author>', methods=['GET'])
def get_author_posts(author):
    """Obtener todos los posts de un autor"""
    posts = Post.find_by_author(author)
    
    return jsonify([post.to_dict() for post in posts]), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)