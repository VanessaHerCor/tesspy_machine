"""
Comando de Django: python manage.py init_users

Inicializa usuarios por defecto en MongoDB si la colección está vacía.
"""
from django.core.management.base import BaseCommand
from auth_api.models import User


class Command(BaseCommand):
    help = '🔧 Inicializa usuarios por defecto en MongoDB'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Inicializando usuarios...'))
        
        try:
            User.initialize_users()
            self.stdout.write(self.style.SUCCESS('✅ Usuarios inicializados correctamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
