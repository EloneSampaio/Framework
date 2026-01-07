"""
Script auxiliar para monitorar uso da GPU durante execução do pipeline.
"""

import subprocess
import sys
from pathlib import Path

def get_gpu_info():
    """Obtém informações da GPU usando nvidia-smi."""
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu', 
             '--format=csv,noheader,nounits'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def monitor_gpu(interval=5):
    """Monitora GPU continuamente."""
    print("Monitorando GPU... (Ctrl+C para parar)")
    print("-" * 60)
    
    try:
        while True:
            gpu_info = get_gpu_info()
            if gpu_info:
                name, mem_used, mem_total, util, temp = gpu_info.split(', ')
                mem_percent = (float(mem_used) / float(mem_total)) * 100
                
                print(f"\rGPU: {name}")
                print(f"  Memória: {mem_used}MB / {mem_total}MB ({mem_percent:.1f}%)")
                print(f"  Utilização: {util}%")
                print(f"  Temperatura: {temp}°C")
                print("-" * 60)
            else:
                print("GPU não detectada ou nvidia-smi não disponível")
                break
            
            import time
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoramento interrompido.")

def check_gpu_available():
    """Verifica se GPU está disponível e retorna informações básicas."""
    gpu_info = get_gpu_info()
    if gpu_info:
        name, mem_used, mem_total, util, temp = gpu_info.split(', ')
        mem_free = float(mem_total) - float(mem_used)
        mem_free_gb = mem_free / 1024
        
        print("✅ GPU Detectada!")
        print(f"  Modelo: {name}")
        print(f"  Memória Total: {float(mem_total)/1024:.1f} GB")
        print(f"  Memória Livre: {mem_free_gb:.1f} GB")
        print(f"  Utilização Atual: {util}%")
        print(f"  Temperatura: {temp}°C")
        
        if mem_free_gb < 2:
            print("\n⚠️  AVISO: Pouca memória GPU livre!")
            print("   Considere reduzir batch size ou limpar cache.")
        
        return True
    else:
        print("❌ GPU não detectada")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "monitor":
        monitor_gpu()
    else:
        check_gpu_available()

