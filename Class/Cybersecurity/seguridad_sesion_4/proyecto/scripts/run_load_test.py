"""
Script para automatizar load testing con diferentes escenarios
"""

import subprocess
import time
import requests
import signal
import os
import sys
from pathlib import Path

class LoadTestRunner:
    """Automatiza ejecución de load tests con diferentes configuraciones"""
    
    def __init__(self, host="http://localhost:5000"):
        self.host = host
        self.server_process = None
    
    def check_server_health(self) -> bool:
        """Verifica que el servidor esté respondiendo"""
        try:
            response = requests.get(f"{self.host}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def start_server_if_needed(self):
        """Inicia servidor si no está corriendo"""
        if self.check_server_health():
            print(f"✅ Server already running at {self.host}")
            return
        
        print(f"🚀 Starting server at {self.host}...")
        self.server_process = subprocess.Popen([
            sys.executable, "src/app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Esperar a que el servidor inicie
        for i in range(30):  # Máximo 30 segundos
            if self.check_server_health():
                print(f"✅ Server started successfully")
                return
            time.sleep(1)
        
        raise Exception("Failed to start server")
    
    def stop_server(self):
        """Detiene servidor si fue iniciado por este script"""
        if self.server_process:
            print("🛑 Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
    
    def run_load_test(self, users: int, duration: str, description: str):
        """Ejecuta load test con configuración específica"""
        print(f"\n🔄 {description}")
        print(f"Users: {users}, Duration: {duration}")
        
        cmd = [
            "locust",
            "-f", "locustfile.py",
            "--host", self.host,
            "--users", str(users),
            "--spawn-rate", str(min(users // 10, 10)),  # Spawn rate razonable
            "--run-time", duration,
            "--headless",  # Sin interfaz web
            "--html", f"reports/load_test_{users}users_{duration.replace('m', 'min')}.html"
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration_actual = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} - Completed ({duration_actual:.1f}s)")
            
            # Extraer métricas básicas del output
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'Aggregated' in line or 'Total' in line:
                    print(f"📊 {line.strip()}")
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
    
    def run_test_suite(self):
        """Ejecuta suite completa de load tests"""
        try:
            self.start_server_if_needed()
            
            print("\n" + "="*60)
            print("LOAD TESTING SUITE")
            print("="*60)
            
            # 1. Smoke load test
            self.run_load_test(
                users=5,
                duration="1m",
                description="Smoke load test (light load verification)"
            )
            
            # 2. Normal load test
            self.run_load_test(
                users=20,
                duration="3m",
                description="Normal load test (typical usage)"
            )
            
            # 3. Stress test
            self.run_load_test(
                users=50,
                duration="2m",
                description="Stress test (high load)"
            )
            
            # 4. Spike test (rápido pero intenso)
            self.run_load_test(
                users=100,
                duration="30s",
                description="Spike test (sudden load increase)"
            )
            
            print("\n" + "="*60)
            print("🎉 LOAD TESTING COMPLETED")
            print("="*60)
            print("📊 Reports generated in reports/ directory")
            print("📋 Review HTML reports for detailed metrics")
            
        finally:
            self.stop_server()

def main():
    """Función principal"""
    # Crear directorio de reportes
    Path("reports").mkdir(exist_ok=True)
    
    runner = LoadTestRunner()
    
    # Manejar Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Load testing interrupted")
        runner.stop_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        runner.run_test_suite()
    except Exception as e:
        print(f"❌ Load testing failed: {e}")
        runner.stop_server()
        sys.exit(1)

if __name__ == "__main__":
    main()