"""
Configuração automática de caminhos para Colab ou ambiente local.
"""

import os
from pathlib import Path

def detect_environment():
    """Detecta se está rodando no Google Colab ou localmente."""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def get_paths():
    """
    Retorna dicionário com todos os caminhos configurados.
    
    Returns:
        dict: Dicionário com caminhos e flags de ambiente
    """
    IN_COLAB = detect_environment()
    
    if IN_COLAB:
        # Caminhos para Google Colab
        BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
        FRAMEWORK_DIR = BASE_DIR / "Framework"
        DATA_DIR = BASE_DIR / "datasets" / "processed"
        FEATURES_DIR = BASE_DIR / "features"
        RESULTS_DIR = BASE_DIR / "results"
        MLRUNS_DIR = BASE_DIR / "mlruns"
        REPOS_DIR = BASE_DIR / "repositories"
    else:
        # Caminhos para ambiente local
        BASE_DIR = Path("../")
        FRAMEWORK_DIR = BASE_DIR
        DATA_DIR = BASE_DIR / "data" / "processed"
        FEATURES_DIR = BASE_DIR / "features"
        RESULTS_DIR = BASE_DIR / "results"
        MLRUNS_DIR = BASE_DIR / "mlruns"
        REPOS_DIR = BASE_DIR / "repositories"
    
    # Criar diretórios se não existirem
    for dir_path in [FEATURES_DIR, RESULTS_DIR, MLRUNS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    return {
        'IN_COLAB': IN_COLAB,
        'BASE_DIR': BASE_DIR,
        'FRAMEWORK_DIR': FRAMEWORK_DIR,
        'DATA_DIR': DATA_DIR,
        'FEATURES_DIR': FEATURES_DIR,
        'RESULTS_DIR': RESULTS_DIR,
        'MLRUNS_DIR': MLRUNS_DIR,
        'REPOS_DIR': REPOS_DIR
    }

def get_batch_sizes():
    """
    Retorna batch sizes otimizados baseado no ambiente.
    
    Returns:
        dict: Dicionário com batch sizes por braço experimental
    """
    IN_COLAB = detect_environment()
    
    if IN_COLAB:
        # Otimizado para T4 (16GB) no Colab
        return {
            "baseline_cnn": 64,
            "vit_pure": 32,
            "vit_contrastive": 16,
            "vit_mim": 8,
            "vit_sparse": 64
        }
    else:
        # Otimizado para RTX 3050 6GB local
        return {
            "baseline_cnn": 32,
            "vit_pure": 16,
            "vit_contrastive": 8,
            "vit_mim": 4,
            "vit_sparse": 32
        }

def setup_environment():
    """
    Configura ambiente completo (monta Drive se Colab, muda diretório, etc.)
    
    Returns:
        dict: Dicionário com caminhos configurados
    """
    IN_COLAB = detect_environment()
    
    if IN_COLAB:
        # Montar Google Drive
        try:
            from google.colab import drive
            drive.mount('/content/drive')
            print("✅ Google Drive montado!")
        except Exception as e:
            print(f"⚠️  Erro ao montar Drive: {e}")
        
        # Mudar para diretório do framework
        paths = get_paths()
        if paths['FRAMEWORK_DIR'].exists():
            os.chdir(paths['FRAMEWORK_DIR'])
            print(f"📁 Mudado para: {paths['FRAMEWORK_DIR']}")
    else:
        print("✅ Ambiente local detectado")
    
    return get_paths()

if __name__ == "__main__":
    # Testar configuração
    paths = setup_environment()
    print("\n📁 Caminhos configurados:")
    for key, value in paths.items():
        if key != 'IN_COLAB':
            print(f"   {key}: {value}")
    
    print(f"\n🖥️  Ambiente: {'Colab' if paths['IN_COLAB'] else 'Local'}")
    
    batch_sizes = get_batch_sizes()
    print("\n📊 Batch sizes configurados:")
    for arm, batch_size in batch_sizes.items():
        print(f"   {arm}: {batch_size}")

