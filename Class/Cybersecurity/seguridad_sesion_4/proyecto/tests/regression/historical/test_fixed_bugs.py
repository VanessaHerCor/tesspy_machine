"""
Tests de regresión para bugs que se arreglaron en el pasado
Estos tests aseguran que los bugs no vuelvan a aparecer
"""

import pytest
from src.data_processor import DataProcessor
from src.report_generator import ReportGenerator

@pytest.mark.regression
class TestHistoricalBugFixes:
    """Tests para bugs específicos que se arreglaron antes"""
    
    def test_bug_001_empty_username_handling(self):
        """
        BUG #001 (Fixed 2024-01-15): Crash cuando username está vacío
        Antes: KeyError cuando username era None o ''
        Ahora: Debe manejar gracefully
        """
        processor = DataProcessor()
        
        # Casos que antes causaban crash
        problematic_users = [
            {'id': 1, 'username': None, 'email': 'test1@example.com'},
            {'id': 2, 'username': '', 'email': 'test2@example.com'},
            {'id': 3, 'email': 'test3@example.com'},  # Sin username
        ]
        
        # No debe lanzar excepción
        processed = processor.process_user_list(problematic_users)
        
        assert len(processed) == 3
        # Debe manejar usernames problemáticos
        assert processed[0]['username'] == ''  # None -> ''
        assert processed[1]['username'] == ''  # '' -> ''
        assert processed[2]['username'] == ''  # Missing -> ''
    
    def test_bug_002_division_by_zero_in_stats(self):
        """
        BUG #002 (Fixed 2024-01-20): División por cero en estadísticas
        Antes: ZeroDivisionError con listas vacías
        Ahora: Debe retornar dict vacío
        """
        processor = DataProcessor()
        
        # Caso que antes causaba ZeroDivisionError
        empty_list = []
        stats = processor.calculate_statistics(empty_list)
        
        # Debe retornar dict vacío, no crash
        assert stats == {}
    
    def test_bug_003_email_domain_extraction_crash(self):
        """
        BUG #003 (Fixed 2024-01-25): Crash extrayendo dominio de email inválido
        Antes: IndexError cuando email no tenía '@'
        Ahora: Debe retornar 'unknown'
        """
        processor = DataProcessor()
        
        # Emails problemáticos que antes causaban crash
        users_with_bad_emails = [
            {'id': 1, 'username': 'user1', 'email': 'notanemail'},
            {'id': 2, 'username': 'user2', 'email': ''},
            {'id': 3, 'username': 'user3'},  # Sin email
        ]
        
        processed = processor.process_user_list(users_with_bad_emails)
        
        # Todos deben tener email_domain = 'unknown'
        for user in processed:
            assert user['email_domain'] == 'unknown'
    
    def test_bug_004_report_percentage_calculation(self):
        """
        BUG #004 (Fixed 2024-02-01): Cálculo erróneo de porcentajes
        Antes: activity_rate mostraba valores incorrectos
        Ahora: Debe calcular correctamente
        """
        generator = ReportGenerator()
        
        # Caso específico que daba resultado incorrecto
        users = [
            {'id': 1, 'username': 'user1', 'email': 'user1@test.com', 'is_active': True},
            {'id': 2, 'username': 'user2', 'email': 'user2@test.com', 'is_active': True},
            {'id': 3, 'username': 'user3', 'email': 'user3@test.com', 'is_active': False},
            {'id': 4, 'username': 'user4', 'email': 'user4@test.com', 'is_active': False},
        ]
        
        report = generator.generate_user_summary(users)
        
        # 2 activos de 4 total = 50%
        assert report['activity_rate'] == 50.0
        assert report['active_users'] == 2
        assert report['inactive_users'] == 2