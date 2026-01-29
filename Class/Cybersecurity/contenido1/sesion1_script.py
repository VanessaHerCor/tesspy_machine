"""
SESIÓN 1: SEGURIDAD EN APLICACIONES WEB
Script de ejemplo: Aplicación Flask con medidas de seguridad básicas

DEPENDENCIAS NECESARIAS:
pip install flask flask-wtf flask-limiter werkzeug marshmallow

INSTRUCCIONES DE EJECUCIÓN:
1. Instalar dependencias: pip install -r requirements.txt
2. Ejecutar: python secure_webapp.py
3. Abrir navegador en: http://localhost:5000

CONCEPTOS DEMOSTRADOS:
- Validación de entrada con Marshmallow
- Hash seguro de passwords
- Protección CSRF
- Rate limiting
- Escape de HTML
- Headers de seguridad
"""

from flask import Flask, render_template_string, request, session, redirect, url_for, jsonify
from flask_wtf import FlaskForm, CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import Schema, fields, ValidationError, validate
import sqlite3
import html
import secrets
import logging
from datetime import datetime

# Configuración de logging para eventos de seguridad
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)
security_logger = logging.getLogger('security')

# Inicialización de Flask con configuración segura
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Clave secreta aleatoria y segura
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # Token CSRF válido por 1 hora

# Protección CSRF activada globalmente
csrf = CSRFProtect(app)

# Rate limiting para prevenir ataques de fuerza bruta
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per hour"]  # Límite general
)

# ================================
# ESQUEMAS DE VALIDACIÓN CON MARSHMALLOW
# ================================

class UserRegistrationSchema(Schema):
    """
    Schema para validar datos de registro de usuario
    Aplica múltiples capas de validación de entrada
    """
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=20),  # Longitud controlada
            validate.Regexp(r'^[a-zA-Z0-9_]+$')  # Solo caracteres alfanuméricos
        ]
    )
    email = fields.Email(required=True)  # Validación de formato de email
    password = fields.Str(
        required=True,
        validate=[
            validate.Length(min=8),  # Mínimo 8 caracteres
            validate.Regexp(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)')  # Al menos 1 minúscula, 1 mayúscula, 1 número
        ]
    )
    
    class Meta:
        unknown = 'EXCLUDE'  # Ignore unknown fields like csrf_token

class UserLoginSchema(Schema):
    """Schema para validar datos de login"""
    username = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    password = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    
    class Meta:
        unknown = 'EXCLUDE'  # Ignore unknown fields like csrf_token

# ================================
# FUNCIONES DE SEGURIDAD
# ================================

def init_db():
    """
    Inicializa la base de datos con tabla de usuarios
    Nota de seguridad: En producción usar migraciones controladas
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    """
    Obtiene conexión segura a la base de datos
    Configuración de SQLite con medidas de seguridad básicas
    """
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
    return conn

def is_safe_redirect(url):
    """
    Valida que una URL de redirección sea segura
    Previene ataques de open redirect
    """
    if not url:
        return False
    return url.startswith('/') or url.startswith(request.host_url)

def log_security_event(event_type, user_data=None, ip_address=None):
    """
    Registra eventos de seguridad para auditoría
    """
    security_logger.info(f"SECURITY_EVENT: {event_type} | User: {user_data} | IP: {ip_address}")

# ================================
# RUTAS DE LA APLICACIÓN
# ================================

@app.before_request
def security_headers():
    """
    Middleware para añadir headers de seguridad HTTP
    Se ejecuta antes de cada request
    """
    pass  # Los headers se añaden en after_request

@app.after_request
def set_security_headers(response):
    """
    Añade headers de seguridad a todas las respuestas
    """
    # Previene ataques XSS
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Content Security Policy básico
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # Fuerza HTTPS en producción
    if app.config.get('ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

@app.route('/')
def index():
    """Página principal con información de seguridad"""
    # Escape automático de datos de sesión para mostrar en plantilla
    username = html.escape(session.get('username', 'Anónimo'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aplicación Web Segura - Demo</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>🛡️ Aplicación Web Segura con Flask</h1>
        <p>Usuario actual: <strong>{{ username }}</strong></p>
        
        {% if 'username' not in session %}
            <h3>Funciones disponibles:</h3>
            <ul>
                <li><a href="/register">📝 Registrarse</a></li>
                <li><a href="/login">🔐 Iniciar sesión</a></li>
            </ul>
        {% else %}
            <h3>¡Bienvenido!</h3>
            <ul>
                <li><a href="/profile">👤 Ver perfil</a></li>
                <li><a href="/logout">🚪 Cerrar sesión</a></li>
            </ul>
        {% endif %}
        
        <hr>
        <h4>🔍 Medidas de seguridad implementadas:</h4>
        <ul>
            <li>✅ Protección CSRF automática</li>
            <li>✅ Validación de entrada con Marshmallow</li>
            <li>✅ Hash seguro de contraseñas</li>
            <li>✅ Rate limiting anti-fuerza bruta</li>
            <li>✅ Headers de seguridad HTTP</li>
            <li>✅ Escape de HTML automático</li>
            <li>✅ Logging de eventos de seguridad</li>
        </ul>
    </body>
    </html>
    '''
    return render_template_string(template, username=username)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Límite específico para registro
def register():
    """
    Registro de usuario con validación completa
    Rate limiting aplicado para prevenir spam
    """
    if request.method == 'GET':
        # Mostrar formulario de registro con token CSRF
        template = '''
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
            <h2>Registro de Usuario</h2>
            <p>Usuario: <input type="text" name="username" required></p>
            <p>Email: <input type="email" name="email" required></p>
            <p>Contraseña: <input type="password" name="password" required></p>
            <p><small>La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número</small></p>
            <button type="submit">Registrarse</button>
        </form>
        <a href="/">← Volver</a>
        '''
        return render_template_string(template)
    
    # Validación de datos POST
    schema = UserRegistrationSchema()
    try:
        # Validar datos de entrada
        data = schema.load(request.form)
    except ValidationError as errors:
        log_security_event("INVALID_REGISTRATION_DATA", 
                          user_data=request.form.get('username'), 
                          ip_address=get_remote_address())
        return jsonify({"error": "Datos inválidos", "details": errors.messages}), 400
    
    # Verificar que el usuario no existe
    conn = get_db_connection()
    existing_user = conn.execute(
        'SELECT id FROM users WHERE username = ? OR email = ?',
        (data['username'], data['email'])
    ).fetchone()
    
    if existing_user:
        conn.close()
        log_security_event("DUPLICATE_REGISTRATION_ATTEMPT", 
                          user_data=data['username'], 
                          ip_address=get_remote_address())
        return jsonify({"error": "Usuario o email ya existe"}), 400
    
    # Hash seguro de la contraseña
    password_hash = generate_password_hash(
        data['password'],
        method='pbkdf2:sha256:100000'  # 100,000 iteraciones para mayor seguridad
    )
    
    # Insertar usuario en base de datos
    try:
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (data['username'], data['email'], password_hash)
        )
        conn.commit()
        conn.close()
        
        log_security_event("USER_REGISTERED", user_data=data['username'])
        return jsonify({"success": "Usuario registrado correctamente"})
        
    except sqlite3.Error as e:
        conn.close()
        log_security_event("DATABASE_ERROR_REGISTRATION", 
                          user_data=data['username'], 
                          ip_address=get_remote_address())
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Rate limiting para prevenir ataques de fuerza bruta
def login():
    """
    Login de usuario con protección contra fuerza bruta
    """
    if request.method == 'GET':
        template = '''
        <form method="POST">
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
            <h2>Iniciar Sesión</h2>
            <p>Usuario: <input type="text" name="username" required></p>
            <p>Contraseña: <input type="password" name="password" required></p>
            <button type="submit">Entrar</button>
        </form>
        <a href="/">← Volver</a>
        '''
        return render_template_string(template)
    
    # Validación de datos de login
    schema = UserLoginSchema()
    try:
        data = schema.load(request.form)
    except ValidationError as errors:
        log_security_event("INVALID_LOGIN_DATA", 
                          user_data=request.form.get('username'), 
                          ip_address=get_remote_address())
        return jsonify({"error": "Datos inválidos", "details": errors.messages}), 400
    
    # Buscar usuario en base de datos
    conn = get_db_connection()
    user = conn.execute(
        'SELECT id, username, password_hash FROM users WHERE username = ?',
        (data['username'],)
    ).fetchone()
    conn.close()
    
    # Verificar credenciales
    if user and check_password_hash(user['password_hash'], data['password']):
        # Login exitoso
        session.permanent = True  # Regenerar session ID por seguridad
        session['user_id'] = user['id']
        session['username'] = user['username']
        
        log_security_event("SUCCESSFUL_LOGIN", user_data=user['username'])
        
        # Redirección segura
        next_page = request.args.get('next')
        if next_page and is_safe_redirect(next_page):
            return redirect(next_page)
        return redirect(url_for('index'))
    else:
        # Login fallido
        log_security_event("FAILED_LOGIN_ATTEMPT", 
                          user_data=data['username'], 
                          ip_address=get_remote_address())
        return jsonify({"error": "Credenciales incorrectas"}), 401

@app.route('/profile')
def profile():
    """
    Página de perfil - requiere autenticación
    Ejemplo de control de acceso básico
    """
    if 'user_id' not in session:
        return redirect(url_for('login', next=request.url))
    
    # Obtener datos del usuario actual
    conn = get_db_connection()
    user = conn.execute(
        'SELECT username, email, created_at FROM users WHERE id = ?',
        (session['user_id'],)
    ).fetchone()
    conn.close()
    
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    # Escape seguro de datos para mostrar
    template = '''
    <h2>Perfil de Usuario</h2>
    <p><strong>Usuario:</strong> {{ username }}</p>
    <p><strong>Email:</strong> {{ email }}</p>
    <p><strong>Registrado:</strong> {{ created_at }}</p>
    <a href="/">← Inicio</a> | <a href="/logout">Cerrar sesión</a>
    '''
    
    return render_template_string(
        template,
        username=html.escape(user['username']),
        email=html.escape(user['email']),
        created_at=user['created_at']
    )

@app.route('/logout')
def logout():
    """
    Cierre de sesión seguro
    """
    if 'username' in session:
        log_security_event("USER_LOGOUT", user_data=session['username'])
    
    session.clear()  # Limpiar toda la sesión
    return redirect(url_for('index'))

# ================================
# INICIALIZACIÓN Y EJECUCIÓN
# ================================

if __name__ == '__main__':
    # Inicializar base de datos
    init_db()
    
    # Configuración de desarrollo (cambiar para producción)
    app.run(
        host='127.0.0.1',  # Solo localhost en desarrollo
        port=5000,
        debug=False,       # NUNCA debug=True en producción
        ssl_context=None   # En producción usar SSL/TLS
    )

"""
NOTAS ADICIONALES DE SEGURIDAD:

1. CONFIGURACIÓN DE PRODUCCIÓN:
   - Usar variables de entorno para SECRET_KEY
   - Configurar base de datos externa (PostgreSQL, MySQL)
   - Implementar HTTPS obligatorio
   - Usar servidor WSGI (Gunicorn, uWSGI)

2. MEDIDAS ADICIONALES A CONSIDERAR:
   - Autenticación de dos factores (2FA)
   - Cifrado de datos sensibles en base de datos
   - Monitoreo de intrusion detection
   - Backup y recovery procedures
   - Auditoría de logs de seguridad

3. TESTING DE SEGURIDAD:
   - Usar herramientas como OWASP ZAP
   - Realizar penetration testing
   - Análisis estático con Bandit
   - Revisar dependencias con Safety

4. COMPLIANCE:
   - Cumplir con GDPR/LOPD para datos personales
   - Implementar políticas de retención de datos
   - Documentar procedimientos de seguridad
"""