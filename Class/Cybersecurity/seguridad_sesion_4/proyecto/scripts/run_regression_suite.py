"""
Script para ejecutar suite completa de regresión
Automatiza diferentes tipos de pruebas en orden apropiado
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Ejecuta comando y retorna True si es exitoso"""
    print(f"\n🔄 {description}")
    print(f"Command: {cmd}")
    
    start_time = time.time()
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    duration = time.time() - start_time
    
    if result.returncode == 0:
        print(f"✅ {description} - OK ({duration:.2f}s)")
        return True
    else:
        print(f"❌ {description} - FAILED ({duration:.2f}s)")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

def main():
    """Ejecuta suite completa de regresión"""
    print("🚀 Starting comprehensive regression testing suite")
    
    # 1. Smoke Tests (críticos, deben pasar primero)
    print("\n" + "="*60)
    print("PHASE 1: SMOKE TESTS (Critical)")
    print("="*60)
    
    if not run_command(
        "pytest tests/smoke/ -v --maxfail=1 --tb=short",
        "Smoke tests (critical functionality)"
    ):
        print("\n💥 CRITICAL: Smoke tests failed! Stopping execution.")
        print("Fix critical issues before continuing with regression suite.")
        sys.exit(1)
    
    # 2. Golden Tests (detectar cambios no intencionales)
    print("\n" + "="*60)
    print("PHASE 2: GOLDEN TESTS (Behavior verification)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/golden/ -v",
        "Golden tests (output verification)"
    )
    
    # 3. Historical Regression (bugs del pasado)
    print("\n" + "="*60)
    print("PHASE 3: HISTORICAL REGRESSION (Bug prevention)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/historical/ -v",
        "Historical bug regression tests"
    )
    
    # 4. Performance Regression (detectar degradación)
    print("\n" + "="*60)
    print("PHASE 4: PERFORMANCE REGRESSION (Speed verification)")
    print("="*60)
    
    run_command(
        "pytest tests/regression/performance/ --benchmark-only --benchmark-sort=mean",
        "Performance regression benchmarks"
    )
    
    # 5. Generar reportes
    print("\n" + "="*60)
    print("PHASE 5: REPORTING")
    print("="*60)
    
    run_command(
        "pytest tests/regression/ --html=reports/regression_report.html --self-contained-html",
        "Generate HTML regression report"
    )
    
    run_command(
        "pytest tests/regression/ --cov=src --cov-report=html:reports/coverage",
        "Generate coverage report"
    )
    
    print("\n" + "="*60)
    print("🎉 REGRESSION SUITE COMPLETED")
    print("="*60)
    print("📊 Reports generated:")
    print("  - HTML Report: reports/regression_report.html")
    print("  - Coverage: reports/coverage/index.html")
    print("  - Benchmark results in terminal output")
    
    print("\n📋 Next steps:")
    print("  1. Review any failed tests")
    print("  2. Update golden files if intentional changes: pytest --force-regen")
    print("  3. Run load tests: locust -f locustfile.py --host=http://localhost:5000")

if __name__ == "__main__":
    main()