from django.http import HttpResponse

def home(request):
    """Vista que devuelve HTML fijo - sin base de datos"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>🎮 Video Games Database</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eee; min-height: 100vh; }
            header { background: linear-gradient(90deg, #00d4ff 0%, #0f3460 100%); padding: 30px 20px; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); margin-bottom: 40px; }
            header h1 { color: white; font-size: 2.5em; margin-bottom: 15px; }
            .nav-container { max-width: 800px; margin: 0 auto; }
            nav { display: flex; flex-wrap: wrap; gap: 20px; }
            .section { display: inline-block; margin-right: 30px; }
            .section-title { color: white; font-weight: bold; font-size: 0.9em; margin-bottom: 8px; }
            nav a { color: white; text-decoration: none; font-weight: bold; padding: 8px 15px; border-radius: 5px; transition: all 0.3s; }
            nav a:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
            .container { max-width: 800px; margin: 0 auto; background: #0f1b2e; padding: 40px; border-radius: 10px; box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1); }
            h1 { color: #00d4ff; }
            h2 { color: #00d4ff; margin-bottom: 20px; font-size: 2em; }
            h3 { color: #00d4ff; margin-top: 20px; }
            .cta-buttons { margin-top: 30px; display: flex; gap: 15px; flex-wrap: wrap; }
            .cta-button { padding: 12px 25px; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
            .btn-dynamic { background: #00d4ff; color: #1a1a2e; }
            .btn-dynamic:hover { background: #ff006e; color: white; }
            .btn-static { background: #0f3460; color: #00d4ff; border: 2px solid #00d4ff; }
            .btn-static:hover { background: #00d4ff; color: #1a1a2e; }
        </style>
    </head>
    <body>
        <header>
            <div class="nav-container">
                <h1>🎮 Videojuegos</h1>
                <nav>
                    <div class="section">
                        <div class="section-title">📄 ESTÁTICAS</div>
                        <a href="/static-pages/">🏠 Home</a>
                        <a href="/static-pages/about/">ℹ️ About</a>
                        <a href="/static-pages/contact/">📧 Contact</a>
                    </div>
                    <div class="section">
                        <div class="section-title">🎮 DINÁMICAS</div>
                        <a href="/dynamic/">📋 Catálogo</a>
                        <a href="/dynamic/api/videogames/">🔌 API JSON</a>
                    </div>
                </nav>
            </div>
        </header>
        <div class="container">
            <h2>¡Bienvenido a Video Games Database!</h2>
            <p><strong>La mejor plataforma para descubrir videojuegos</strong></p>
            <ul>
                <li>✅ Catálogo completo de videojuegos</li>
                <li>✅ Información actualizada de títulos populares</li>
                <li>✅ Búsqueda rápida y eficiente</li>
                <li>✅ Reseñas y puntuaciones de usuarios</li>
            </ul>
            
            <p><em>Explora miles de videojuegos desde clásicos hasta lanzamientos recientes.</em></p>
            
            <div class="cta-buttons">
                <a href="/dynamic/" class="cta-button btn-dynamic">🎮 Ver Catálogo Dinámico</a>
                <a href="/static-pages/about/" class="cta-button btn-static">ℹ️ Conocer Más</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def about(request):
    """Página About estática"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ℹ️ Acerca de</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eee; min-height: 100vh; }
            header { background: linear-gradient(90deg, #00d4ff 0%, #0f3460 100%); padding: 30px 20px; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); margin-bottom: 40px; }
            header h1 { color: white; font-size: 2.5em; margin-bottom: 15px; }
            .nav-container { max-width: 800px; margin: 0 auto; }
            nav { display: flex; flex-wrap: wrap; gap: 20px; }
            .section { display: inline-block; margin-right: 30px; }
            .section-title { color: white; font-weight: bold; font-size: 0.9em; margin-bottom: 8px; }
            nav a { color: white; text-decoration: none; font-weight: bold; padding: 8px 15px; border-radius: 5px; transition: all 0.3s; }
            nav a:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
            .container { max-width: 800px; margin: 0 auto; background: #0f1b2e; padding: 40px; border-radius: 10px; box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1); }
            h2 { color: #00d4ff; margin-bottom: 20px; font-size: 2em; }
            h3 { color: #00d4ff; margin-top: 20px; }
            .cta-buttons { margin-top: 30px; display: flex; gap: 15px; flex-wrap: wrap; }
            .cta-button { padding: 12px 25px; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
            .btn-dynamic { background: #00d4ff; color: #1a1a2e; }
            .btn-dynamic:hover { background: #ff006e; color: white; }
            .btn-static { background: #0f3460; color: #00d4ff; border: 2px solid #00d4ff; }
            .btn-static:hover { background: #00d4ff; color: #1a1a2e; }
        </style>
    </head>
    <body>
        <header>
            <div class="nav-container">
                <h1>🎮 Videojuegos</h1>
                <nav>
                    <div class="section">
                        <div class="section-title">📄 ESTÁTICAS</div>
                        <a href="/static-pages/">🏠 Home</a>
                        <a href="/static-pages/about/">ℹ️ About</a>
                        <a href="/static-pages/contact/">📧 Contact</a>
                    </div>
                    <div class="section">
                        <div class="section-title">🎮 DINÁMICAS</div>
                        <a href="/dynamic/">📋 Catálogo</a>
                        <a href="/dynamic/api/videogames/">🔌 API JSON</a>
                    </div>
                </nav>
            </div>
        </header>
        <div class="container">
            <h2>ℹ️ Acerca de Video Games Database</h2>
            <h3>Nuestra Misión:</h3>
            <p>Proporcionar la base de datos más completa y actualizada de videojuegos del mundo.</p>
            
            <h3>Características principales:</h3>
            <ul>
                <li>🎯 Base de datos MongoDB para escalabilidad</li>
                <li>🔍 API REST para acceder a información de videojuegos</li>
                <li>⭐ Sistema de calificaciones y reseñas</li>
                <li>🏆 Clasificación por géneros, plataformas y años</li>
                <li>📊 Estadísticas actualizadas en tiempo real</li>
            </ul>
            
            <h3>Tecnología:</h3>
            <p><strong>Django + MongoDB + REST Framework</strong></p>
            
            <div class="cta-buttons">
                <a href="/dynamic/" class="cta-button btn-dynamic">🎮 Ver Catálogo</a>
                <a href="/static-pages/" class="cta-button btn-static">← Volver al Home</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def contact(request):
    """Formulario de contacto estático"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>📧 Contacto</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: #eee; min-height: 100vh; }
            header { background: linear-gradient(90deg, #00d4ff 0%, #0f3460 100%); padding: 30px 20px; box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3); margin-bottom: 40px; }
            header h1 { color: white; font-size: 2.5em; margin-bottom: 15px; }
            .nav-container { max-width: 800px; margin: 0 auto; }
            nav { display: flex; flex-wrap: wrap; gap: 20px; }
            .section { display: inline-block; margin-right: 30px; }
            .section-title { color: white; font-weight: bold; font-size: 0.9em; margin-bottom: 8px; }
            nav a { color: white; text-decoration: none; font-weight: bold; padding: 8px 15px; border-radius: 5px; transition: all 0.3s; }
            nav a:hover { background: rgba(255,255,255,0.2); transform: translateY(-2px); }
            .container { max-width: 800px; margin: 0 auto; background: #0f1b2e; padding: 40px; border-radius: 10px; box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1); }
            h2 { color: #00d4ff; margin-bottom: 20px; font-size: 2em; }
            .form-group { margin: 15px 0; }
            label { color: #00d4ff; font-weight: bold; display: block; margin-bottom: 5px; }
            input, textarea { width: 100%; max-width: 400px; padding: 10px; 
                            background: #0f3460; color: #eee; border: 1px solid #00d4ff; 
                            border-radius: 5px; }
            input:focus, textarea:focus { outline: none; background: #1a4d5e; box-shadow: 0 0 10px #00d4ff; }
            button { background: #00d4ff; color: #1a1a2e; padding: 10px 20px; 
                    border: none; border-radius: 5px; font-weight: bold; cursor: pointer; transition: all 0.3s; }
            button:hover { background: #ff006e; }
            .cta-buttons { margin-top: 30px; display: flex; gap: 15px; flex-wrap: wrap; }
            .cta-button { padding: 12px 25px; border-radius: 5px; text-decoration: none; font-weight: bold; transition: all 0.3s; }
            .btn-dynamic { background: #00d4ff; color: #1a1a2e; }
            .btn-dynamic:hover { background: #ff006e; color: white; }
            .btn-static { background: #0f3460; color: #00d4ff; border: 2px solid #00d4ff; }
            .btn-static:hover { background: #00d4ff; color: #1a1a2e; }
        </style>
    </head>
    <body>
        <header>
            <div class="nav-container">
                <h1>🎮 Videojuegos</h1>
                <nav>
                    <div class="section">
                        <div class="section-title">📄 ESTÁTICAS</div>
                        <a href="/static-pages/">🏠 Home</a>
                        <a href="/static-pages/about/">ℹ️ About</a>
                        <a href="/static-pages/contact/">📧 Contact</a>
                    </div>
                    <div class="section">
                        <div class="section-title">🎮 DINÁMICAS</div>
                        <a href="/dynamic/">📋 Catálogo</a>
                        <a href="/dynamic/api/videogames/">🔌 API JSON</a>
                    </div>
                </nav>
            </div>
        </header>
        <div class="container">
            <h2>📧 Contacto</h2>
            <p><strong>¿Tienes una pregunta sobre videojuegos?</strong></p>
            <p>Completa el formulario y nos pondremos en contacto pronto.</p>
            
            <form>
                <div class="form-group">
                    <label>Nombre:</label>
                    <input type="text" placeholder="Tu nombre" required>
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" placeholder="tu@email.com" required>
                </div>
                <div class="form-group">
                    <label>Asunto:</label>
                    <input type="text" placeholder="¿Sobre qué es tu consulta?" required>
                </div>
                <div class="form-group">
                    <label>Mensaje:</label>
                    <textarea rows="5" placeholder="Cuéntanos más..."></textarea>
                </div>
                <button type="button" onclick="alert('¡Gracias por tu mensaje! Te contactaremos pronto.')">
                    📤 Enviar Mensaje
                </button>
            </form>
            
            <div class="cta-buttons">
                <a href="/dynamic/" class="cta-button btn-dynamic">🎮 Ver Catálogo</a>
                <a href="/static-pages/" class="cta-button btn-static">← Volver al Home</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)
