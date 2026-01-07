"""
Script de setup para Google Colab.
Execute esta célula no início de cada notebook no Colab.
"""

import os
import sys
from pathlib import Path

def setup_colab_environment():
    """Configura ambiente do Google Colab."""
    
    print("="*60)
    print("🚀 CONFIGURAÇÃO INICIAL - GOOGLE COLAB")
    print("="*60)
    
    # 1. Montar Google Drive
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive montado!")
    except ImportError:
        print("⚠️  Não está rodando no Colab. Pulando montagem do Drive.")
        return None
    except Exception as e:
        print(f"⚠️  Erro ao montar Drive: {e}")
        return None
    
    # 2. Configurar caminhos
    BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
    FRAMEWORK_DIR = BASE_DIR / "Framework"
    DATA_DIR = BASE_DIR / "datasets"
    REPOS_DIR = BASE_DIR / "repositories"
    FEATURES_DIR = BASE_DIR / "features"
    RESULTS_DIR = BASE_DIR / "results"
    MLRUNS_DIR = BASE_DIR / "mlruns"
    
    # 3. Criar diretórios
    for dir_path in [BASE_DIR, FRAMEWORK_DIR, DATA_DIR, REPOS_DIR, 
                     FEATURES_DIR, RESULTS_DIR, MLRUNS_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # 4. Mudar para diretório do framework
    if FRAMEWORK_DIR.exists():
        os.chdir(FRAMEWORK_DIR)
        print(f"✅ Mudado para: {FRAMEWORK_DIR}")
    else:
        print(f"⚠️  Diretório do framework não encontrado: {FRAMEWORK_DIR}")
        print("   Certifique-se de fazer upload dos notebooks para o Drive")
    
    # 5. Verificar GPU
    try:
        import tensorflow as tf
        
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"\n✅ GPU detectada: {len(gpus)} GPU(s)")
            for i, gpu in enumerate(gpus):
                print(f"   GPU {i}: {gpu}")
            
            # Configurar memória GPU
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                print("✅ Memória GPU configurada para crescimento dinâmico")
            except RuntimeError as e:
                print(f"⚠️  Erro ao configurar GPU: {e}")
        else:
            print("\n⚠️  Nenhuma GPU detectada!")
            print("   Vá em Runtime > Change runtime type > GPU")
    except ImportError:
        print("\n⚠️  TensorFlow não instalado ainda")
    
    # 6. Informações do sistema
    print("\n📁 Estrutura de Diretórios:")
    print(f"   Base: {BASE_DIR}")
    print(f"   Framework: {FRAMEWORK_DIR}")
    print(f"   Datasets: {DATA_DIR}")
    print(f"   Features: {FEATURES_DIR}")
    print(f"   Results: {RESULTS_DIR}")
    print(f"   MLflow: {MLRUNS_DIR}")
    
    return {
        'BASE_DIR': BASE_DIR,
        'FRAMEWORK_DIR': FRAMEWORK_DIR,
        'DATA_DIR': DATA_DIR,
        'REPOS_DIR': REPOS_DIR,
        'FEATURES_DIR': FEATURES_DIR,
        'RESULTS_DIR': RESULTS_DIR,
        'MLRUNS_DIR': MLRUNS_DIR
    }

def install_dependencies():
    """Instala dependências necessárias."""
    
    print("\n" + "="*60)
    print("📦 INSTALANDO DEPENDÊNCIAS")
    print("="*60)
    
    packages = [
        "mlflow",
        "scikit-posthocs",
        "nibabel",
        "transformers",
        "tensorflow",
        "scikit-learn",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "GPUtil"  # Para monitoramento
    ]
    
    for package in packages:
        print(f"Instalando {package}...")
        os.system(f"pip install -q {package}")
    
    print("\n✅ Todas as dependências instaladas!")

def clone_repositories():
    """Clona repositórios necessários."""
    
    print("\n" + "="*60)
    print("📥 CLONANDO REPOSITÓRIOS")
    print("="*60)
    
    REPOS_DIR = Path("/content/drive/MyDrive/Mestrado_TCC/repositories")
    REPOS_DIR.mkdir(parents=True, exist_ok=True)
    
    repos = {
        "domain_specific_cl": "https://github.com/krishnabits001/domain_specific_cl",
        "MIM-Med3D": "https://github.com/chenz53/MIM-Med3D"
    }
    
    for repo_name, repo_url in repos.items():
        repo_path = REPOS_DIR / repo_name
        if repo_path.exists():
            print(f"✅ {repo_name} já existe")
        else:
            print(f"📥 Clonando {repo_name}...")
            os.system(f"cd {REPOS_DIR} && git clone {repo_url}")
            print(f"✅ {repo_name} clonado!")
    
    print("\n✅ Repositórios prontos!")

if __name__ == "__main__":
    # Executar setup
    paths = setup_colab_environment()
    
    if paths:
        # Instalar dependências
        install_dependencies()
        
        # Clonar repositórios
        clone_repositories()
        
        print("\n" + "="*60)
        print("✅ SETUP COMPLETO!")
        print("="*60)
        print("\nPróximos passos:")
        print("1. Verifique se os datasets estão no Drive")
        print("2. Execute os notebooks na ordem:")
        print("   - 01_Download_Datasets.ipynb")
        print("   - 02_Feature_Extraction.ipynb")
        print("   - 03_Classification.ipynb")
        print("   - 04_Avaliacao_Estatistica.ipynb")
    else:
        print("\n⚠️  Setup não completado. Verifique se está no Colab.")

