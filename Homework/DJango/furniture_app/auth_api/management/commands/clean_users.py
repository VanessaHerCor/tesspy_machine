"""
Comando de Django: python manage.py clean_users

Limpia la colección de usuarios en MongoDB y reinicializa.
"""
from django.core.management.base import BaseCommand
from auth_api.models import User


class Command(BaseCommand):
    help = '🧹 Limpia y reinicializa usuarios en MongoDB'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🧹 Limpiando colección de usuarios...'))
        
        try:
            User.drop_collection()
            self.stdout.write(self.style.SUCCESS('✅ Colección eliminada'))
            
            User.initialize_users()
            self.stdout.write(self.style.SUCCESS('✅ Usuarios reinicializados correctamente'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
