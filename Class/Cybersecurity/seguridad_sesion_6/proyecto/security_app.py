"""
Sesión 6: Pruebas de seguridad y protección contra ataques
Aplicación web con vulnerabilidades intencionales para demonstrar security testing
"""

from flask import Flask, request, jsonify, session, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import secrets
import time
import re
import html
import jwt
from datetime import datetime, timedelta
from functools import wraps
import hashlib
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Configuración de seguridad
FAILED_LOGIN_ATTEMPTS = {}
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutos

# Base de datos en memoria para testing
class Database:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Inicializa base de datos con datos de prueba"""
        self.conn = sqlite3.connect(':memory:', check_same_thread=False)
        self.conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TIMESTAMP NULL
            )
        ''')
        
        self.conn.execute('''
            CREATE TABLE posts (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                author_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        ''')
        
        # Crear usuarios de prueba
        admin_hash = generate_password_hash('admin123!')
        user_hash = generate_password_hash('user123!')
        
        self.conn.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('admin', 'admin@example.com', admin_hash, 'admin')
        )
        self.conn.execute(
            "INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ('testuser', 'user@example.com', user_hash, 'user')
        )
        
        # Posts de prueba
        self.conn.execute(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            ('Post público', 'Este es un post visible para todos', 2)
        )
        self.conn.execute(
            "INSERT INTO posts (title, content, author_id) VALUES (?, ?, ?)",
            ('Post admin', 'Este post contiene información sensible', 1)
        )
        
        self.conn.commit()

db = Database()

# Decoradores de autenticación y autorización
def token_required(f):
    """Decorator para endpoints que requieren autenticación"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token required'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator para endpoints que requieren privilegios de admin"""
    @wraps(f)
    def decorated(current_user_id, *args, **kwargs):
        cursor = db.conn.execute(
            "SELECT role FROM users WHERE id = ?", (current_user_id,)
        )
        user = cursor.fetchone()
        
        if not user or user[0] != 'admin':
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(current_user_id, *args, **kwargs)
    return decorated

# Endpoints de autenticación
@app.route('/auth/register', methods=['POST'])
def register():
    """Registro de usuarios con validación básica"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    email = data.get('email', f"{username}@example.com")
    
    # Validación de password
    if len(password) < 8:
        return jsonify({'error': 'Password must be at least 8 characters'}), 400
    
    try:
        password_hash = generate_password_hash(password)
        db.conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        db.conn.commit()
        
        return jsonify({'message': 'User created successfully'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409

@app.route('/auth/login', methods=['POST'])
def login():
    """Login con protección contra brute force"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400
    
    username = data['username']
    password = data['password']
    client_ip = request.remote_addr
    
    # Verificar si IP está bloqueada
    if client_ip in FAILED_LOGIN_ATTEMPTS:
        attempts_data = FAILED_LOGIN_ATTEMPTS[client_ip]
        if attempts_data['count'] >= MAX_LOGIN_ATTEMPTS:
            if time.time() - attempts_data['last_attempt'] < LOCKOUT_DURATION:
                return jsonify({'error': 'Too many failed attempts. Try again later.'}), 429
            else:
                # Reset counter después del lockout
                del FAILED_LOGIN_ATTEMPTS[client_ip]
    
    # Buscar usuario
    cursor = db.conn.execute(
        "SELECT id, username, password_hash, role, locked_until FROM users WHERE username = ?",
        (username,)
    )
    user = cursor.fetchone()
    
    if not user or not check_password_hash(user[2], password):
        # Registrar intento fallido
        if client_ip not in FAILED_LOGIN_ATTEMPTS:
            FAILED_LOGIN_ATTEMPTS[client_ip] = {'count': 0, 'last_attempt': 0}
        
        FAILED_LOGIN_ATTEMPTS[client_ip]['count'] += 1
        FAILED_LOGIN_ATTEMPTS[client_ip]['last_attempt'] = time.time()
        
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Login exitoso - limpiar intentos fallidos
    if client_ip in FAILED_LOGIN_ATTEMPTS:
        del FAILED_LOGIN_ATTEMPTS[client_ip]
    
    # Generar JWT token
    token_payload = {
        'user_id': user[0],
        'username': user[1],
        'role': user[3],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(token_payload, app.secret_key, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'user': {
            'id': user[0],
            'username': user[1],
            'role': user[3]
        }
    }), 200

# Endpoints con diferentes vulnerabilidades para testing
@app.route('/search', methods=['GET'])
def search_vulnerable():
    """
    VULNERABLE: SQL Injection endpoint para testing
    NO USAR EN PRODUCCIÓN
    """
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'results': [], 'query': query}), 200
    
    # VULNERABLE: SQL injection directo
    sql = f"SELECT title, content FROM posts WHERE title LIKE '%{query}%' OR content LIKE '%{query}%'"
    
    try:
        cursor = db.conn.execute(sql)
        results = [{'title': row[0], 'content': row[1]} for row in cursor.fetchall()]
        return jsonify({'results': results, 'query': query}), 200
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@app.route('/search-safe', methods=['GET'])
def search_safe():
    """Versión segura del endpoint de búsqueda"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'results': [], 'query': query}), 200
    
    # SEGURO: Usar parámetros preparados
    cursor = db.conn.execute(
        "SELECT title, content FROM posts WHERE title LIKE ? OR content LIKE ?",
        (f'%{query}%', f'%{query}%')
    )
    results = [{'title': row[0], 'content': row[1]} for row in cursor.fetchall()]
    
    return jsonify({'results': results, 'query': query}), 200

@app.route('/comment', methods=['POST'])
def add_comment_vulnerable():
    """
    VULNERABLE: XSS endpoint para testing
    NO USAR EN PRODUCCIÓN
    """
    data = request.get_json()
    content = data.get('content', '')
    
    # VULNERABLE: No sanitiza HTML
    return jsonify({
        'message': 'Comment added',
        'content': content,  # XSS vulnerable
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@app.route('/comment-safe', methods=['POST'])
def add_comment_safe():
    """Versión segura del endpoint de comentarios"""
    data = request.get_json()
    content = data.get('content', '')
    
    # SEGURO: Escapar HTML
    safe_content = html.escape(content)
    
    return jsonify({
        'message': 'Comment added',
        'content': safe_content,
        'timestamp': datetime.utcnow().isoformat()
    }), 201

@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user_id, user_id):
    """
    VULNERABLE: Insecure Direct Object Reference
    Los usuarios pueden acceder a datos de otros usuarios
    """
    cursor = db.conn.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # VULNERABLE: No verifica si el usuario actual puede ver estos datos
    return jsonify({
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'role': user[3]
    }), 200

@app.route('/users-safe/<int:user_id>', methods=['GET'])
@token_required
def get_user_safe(current_user_id, user_id):
    """Versión segura que verifica autorización"""
    # SEGURO: Verificar que el usuario solo puede ver sus propios datos
    # o que sea admin
    cursor = db.conn.execute(
        "SELECT role FROM users WHERE id = ?", (current_user_id,)
    )
    current_user = cursor.fetchone()
    
    if current_user_id != user_id and current_user[0] != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    cursor = db.conn.execute(
        "SELECT id, username, email, role FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user[0],
        'username': user[1],
        'email': user[2],
        'role': user[3]
    }), 200

@app.route('/admin/users', methods=['GET'])
@token_required
@admin_required
def list_all_users(current_user_id):
    """Endpoint solo para administradores"""
    cursor = db.conn.execute(
        "SELECT id, username, email, role, created_at FROM users"
    )
    users = []
    for row in cursor.fetchall():
        users.append({
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'role': row[3],
            'created_at': row[4]
        })
    
    return jsonify({'users': users}), 200

@app.route('/file/<path:filename>', methods=['GET'])
def get_file_vulnerable(filename):
    """
    VULNERABLE: Path traversal
    NO USAR EN PRODUCCIÓN
    """
    # VULNERABLE: No valida el path
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/file-safe/<filename>', methods=['GET'])
def get_file_safe(filename):
    """Versión segura que previene path traversal"""
    # SEGURO: Validar filename y usar directorio seguro
    if not re.match(r'^[a-zA-Z0-9._-]+$', filename):
        return jsonify({'error': 'Invalid filename'}), 400
    
    safe_dir = '/tmp/safe_files'  # Directorio seguro
    safe_path = os.path.join(safe_dir, filename)
    
    # Verificar que el path esté dentro del directorio seguro
    if not safe_path.startswith(safe_dir):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        with open(safe_path, 'r') as f:
            content = f.read()
        return jsonify({'filename': filename, 'content': content}), 200
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }), 200

# Headers de seguridad
@app.after_request
def add_security_headers(response):
    """Agregar headers de seguridad"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    print("🔐 SECURITY TESTING APPLICATION")
    print("=" * 40)
    print("ENDPOINTS DISPONIBLES:")
    print("📝 Authentication:")
    print("  POST /auth/register - Registro de usuario")
    print("  POST /auth/login - Login con protección brute force")
    print()
    print("🚨 VULNERABLE ENDPOINTS (para testing):")
    print("  GET  /search?q=<query> - SQL Injection vulnerable")
    print("  POST /comment - XSS vulnerable")
    print("  GET  /users/<id> - IDOR vulnerable")
    print("  GET  /file/<path> - Path traversal vulnerable")
    print()
    print("✅ SECURE ENDPOINTS:")
    print("  GET  /search-safe?q=<query> - SQL Injection protegido")
    print("  POST /comment-safe - XSS protegido")
    print("  GET  /users-safe/<id> - IDOR protegido")
    print("  GET  /file-safe/<filename> - Path traversal protegido")
    print("  GET  /admin/users - Solo admin (requiere token)")
    print()
    print("⚠️  PARA TESTING SEGURO ÚNICAMENTE!")
    print("⚠️  NO USAR ENDPOINTS VULNERABLES EN PRODUCCIÓN!")
    
    app.run(host='0.0.0.0', port=5001, debug=False)