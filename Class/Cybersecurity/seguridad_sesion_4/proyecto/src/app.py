"""
API Flask simple para demostrar load testing
Incluye endpoints con diferentes características de rendimiento
"""

from flask import Flask, jsonify, request, abort
import time
import random
import threading
from datetime import datetime
from typing import Dict, List
import json

app = Flask(__name__)

# Simulación de base de datos en memoria
users_db = {}
posts_db = {}
sessions = {}
request_count = 0
request_lock = threading.Lock()

def get_request_stats():
    """Obtiene estadísticas de requests para monitoring"""
    with request_lock:
        return request_count

@app.before_request
def track_requests():
    """Middleware para contar requests"""
    global request_count
    with request_lock:
        request_count += 1

@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check - crítico para smoke tests
    Debe responder siempre en <100ms
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    """
    Endpoint rápido para listar usuarios
    Simula consulta simple a BD
    """
    # Simular latencia de BD (50-100ms)
    time.sleep(random.uniform(0.05, 0.1))
    
    return jsonify({
        'users': list(users_db.values()),
        'total': len(users_db),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Endpoint para crear usuario
    Simula operación de escritura más lenta
    """
    data = request.get_json()
    if not data or 'username' not in data:
        abort(400, 'Username is required')
    
    username = data['username']
    if username in users_db:
        abort(409, 'User already exists')
    
    # Simular validación y escritura a BD (100-200ms)
    time.sleep(random.uniform(0.1, 0.2))
    
    user_id = len(users_db) + 1
    user = {
        'id': user_id,
        'username': username,
        'email': data.get('email', f'{username}@example.com'),
        'created_at': datetime.utcnow().isoformat()
    }
    users_db[user_id] = user
    
    return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Endpoint para obtener usuario específico
    Incluye posibilidad de error 404
    """
    # Simular latencia de consulta
    time.sleep(random.uniform(0.03, 0.08))
    
    if user_id not in users_db:
        abort(404, 'User not found')
    
    return jsonify(users_db[user_id]), 200

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Endpoint con paginación - útil para load testing
    Simula consulta más compleja
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Simular consulta compleja (100-300ms)
    time.sleep(random.uniform(0.1, 0.3))
    
    # Simular paginación
    total_posts = len(posts_db)
    start = (page - 1) * per_page
    end = start + per_page
    posts_slice = list(posts_db.values())[start:end]
    
    return jsonify({
        'posts': posts_slice,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total_posts,
            'pages': (total_posts + per_page - 1) // per_page
        }
    }), 200

@app.route('/api/search', methods=['GET'])
def search():
    """
    Endpoint de búsqueda - operación costosa
    Ideal para stress testing
    """
    query = request.args.get('q', '')
    if not query:
        abort(400, 'Query parameter q is required')
    
    # Simular búsqueda compleja (200-500ms)
    time.sleep(random.uniform(0.2, 0.5))
    
    # Simular resultados basados en query
    results = []
    for user in users_db.values():
        if query.lower() in user['username'].lower():
            results.append(user)
    
    return jsonify({
        'query': query,
        'results': results,
        'total': len(results),
        'execution_time_ms': random.randint(200, 500)
    }), 200

@app.route('/api/heavy-operation', methods=['POST'])
def heavy_operation():
    """
    Endpoint que simula operación pesada
    Para testing de límites y timeouts
    """
    # Simular operación muy lenta (1-3 segundos)
    time.sleep(random.uniform(1.0, 3.0))
    
    # 10% de probabilidad de error para simular condiciones reales
    if random.random() < 0.1:
        abort(500, 'Internal server error during heavy operation')
    
    return jsonify({
        'status': 'completed',
        'processing_time': random.uniform(1.0, 3.0),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Endpoint para obtener estadísticas del servidor
    Útil para monitoreo durante load testing
    """
    return jsonify({
        'total_requests': get_request_stats(),
        'total_users': len(users_db),
        'total_posts': len(posts_db),
        'active_sessions': len(sessions),
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.route('/api/slow', methods=['GET'])
def slow_endpoint():
    """
    Endpoint intencionalmente lento
    Para demonstrar degradación de rendimiento
    """
    # Simular degradación progresiva bajo carga
    current_load = get_request_stats()
    sleep_time = min(0.1 + (current_load * 0.001), 2.0)  # Máximo 2 segundos
    time.sleep(sleep_time)
    
    return jsonify({
        'message': 'This endpoint gets slower under load',
        'current_load': current_load,
        'sleep_time': sleep_time
    }), 200

# Inicializar algunos datos de prueba
def init_test_data():
    """Inicializa datos de prueba para la aplicación"""
    global users_db, posts_db
    
    # Crear usuarios de prueba
    for i in range(1, 11):
        user = {
            'id': i,
            'username': f'user{i}',
            'email': f'user{i}@example.com',
            'created_at': datetime.utcnow().isoformat()
        }
        users_db[i] = user
    
    # Crear posts de prueba
    for i in range(1, 21):
        post = {
            'id': i,
            'title': f'Post {i}',
            'content': f'Content for post {i}',
            'author_id': random.randint(1, 10),
            'created_at': datetime.utcnow().isoformat()
        }
        posts_db[i] = post

if __name__ == '__main__':
    init_test_data()
    print("🚀 Starting Flask server for load testing...")
    print("📊 Available endpoints:")
    print("  GET  /health - Health check")
    print("  GET  /api/users - List users")
    print("  POST /api/users - Create user")
    print("  GET  /api/users/<id> - Get user")
    print("  GET  /api/posts - List posts (paginated)")
    print("  GET  /api/search?q=<query> - Search")
    print("  POST /api/heavy-operation - Heavy operation")
    print("  GET  /api/stats - Server stats")
    print("  GET  /api/slow - Intentionally slow endpoint")
    
    app.run(host='0.0.0.0', port=5001, debug=False, threaded=True)