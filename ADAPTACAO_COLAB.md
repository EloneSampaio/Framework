# 🔄 Adaptação dos Notebooks para Colab

## ⚠️ Importante: Ajustes Necessários

Os notebooks foram criados com caminhos relativos (`../`) que funcionam localmente, mas precisam ser ajustados para o Colab.

---

## 🔧 Solução: Célula de Detecção Automática

Adicione esta célula **no início** de cada notebook (após montar o Drive):

```python
# ============================================
# DETECÇÃO AUTOMÁTICA: COLAB OU LOCAL
# ============================================

import os
from pathlib import Path

# Detectar se está rodando no Colab
try:
    import google.colab
    IN_COLAB = True
    print("✅ Detectado: Google Colab")
except ImportError:
    IN_COLAB = False
    print("✅ Detectado: Ambiente Local")

# Configurar caminhos baseado no ambiente
if IN_COLAB:
    # Caminhos para Colab
    BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
    FRAMEWORK_DIR = BASE_DIR / "Framework"
    DATA_DIR = BASE_DIR / "datasets" / "processed"
    FEATURES_DIR = BASE_DIR / "features"
    RESULTS_DIR = BASE_DIR / "results"
    MLRUNS_DIR = BASE_DIR / "mlruns"
    REPOS_DIR = BASE_DIR / "repositories"
    
    # Mudar para diretório do framework
    if FRAMEWORK_DIR.exists():
        os.chdir(FRAMEWORK_DIR)
        print(f"📁 Mudado para: {FRAMEWORK_DIR}")
else:
    # Caminhos para ambiente local
    BASE_DIR = Path("../")
    DATA_DIR = BASE_DIR / "data" / "processed"
    FEATURES_DIR = BASE_DIR / "features"
    RESULTS_DIR = BASE_DIR / "results"
    MLRUNS_DIR = BASE_DIR / "mlruns"
    REPOS_DIR = BASE_DIR / "repositories"

# Criar diretórios necessários
for dir_path in [FEATURES_DIR, RESULTS_DIR, MLRUNS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

print(f"📁 BASE_DIR: {BASE_DIR}")
print(f"📁 FEATURES_DIR: {FEATURES_DIR}")
print(f"📁 RESULTS_DIR: {RESULTS_DIR}")
```

---

## 📝 Adaptações por Notebook

### Notebook 01_Download_Datasets.ipynb

**Adicionar no início:**
```python
# Célula de detecção (acima)
# Depois, ajustar:
DATA_DIR = BASE_DIR / "datasets"  # Em vez de BASE_DIR / "data"
```

### Notebook 02_Feature_Extraction.ipynb

**Substituir a célula de configuração:**
```python
# REMOVER esta linha:
BASE_DIR = Path("../")

# USAR a detecção automática (célula acima)
# Depois, ajustar batch sizes para Colab:
BATCH_SIZES = {
    "baseline_cnn": 64 if IN_COLAB else 32,
    "vit_pure": 32 if IN_COLAB else 16,
    "vit_contrastive": 16 if IN_COLAB else 8,
    "vit_mim": 8 if IN_COLAB else 4,
    "vit_sparse": 64 if IN_COLAB else 32
}
```

### Notebook 03_Classification.ipynb

**Substituir configuração:**
```python
# REMOVER:
BASE_DIR = Path("../")
FEATURES_DIR = BASE_DIR / "features"

# USAR detecção automática
# FEATURES_DIR já está definido
```

### Notebook 04_Avaliacao_Estatistica.ipynb

**Substituir configuração:**
```python
# REMOVER:
BASE_DIR = Path("../")
RESULTS_DIR = BASE_DIR / "results" / "classifications"

# USAR detecção automática
RESULTS_DIR = RESULTS_DIR / "classifications"  # Ajustar caminho
```

---

## 🎯 Versão Simplificada: Função Helper

Crie uma função helper que pode ser importada:

```python
# Salvar em scripts/utils/path_config.py

def get_paths():
    """Retorna caminhos configurados baseado no ambiente."""
    import os
    from pathlib import Path
    
    try:
        import google.colab
        IN_COLAB = True
    except ImportError:
        IN_COLAB = False
    
    if IN_COLAB:
        BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
        FRAMEWORK_DIR = BASE_DIR / "Framework"
    else:
        BASE_DIR = Path("../")
        FRAMEWORK_DIR = BASE_DIR
    
    return {
        'IN_COLAB': IN_COLAB,
        'BASE_DIR': BASE_DIR,
        'FRAMEWORK_DIR': FRAMEWORK_DIR,
        'DATA_DIR': BASE_DIR / ("datasets" if IN_COLAB else "data") / "processed",
        'FEATURES_DIR': BASE_DIR / "features",
        'RESULTS_DIR': BASE_DIR / "results",
        'MLRUNS_DIR': BASE_DIR / "mlruns",
        'REPOS_DIR': BASE_DIR / "repositories"
    }
```

Depois, nos notebooks:
```python
from utils.path_config import get_paths
paths = get_paths()
BASE_DIR = paths['BASE_DIR']
FEATURES_DIR = paths['FEATURES_DIR']
# etc...
```

---

## ✅ Checklist de Adaptação

Para cada notebook (01-04):

- [ ] Adicionar célula de detecção Colab/Local
- [ ] Substituir `BASE_DIR = Path("../")` pela detecção
- [ ] Ajustar caminhos para usar variáveis da detecção
- [ ] Ajustar batch sizes (se aplicável)
- [ ] Testar no Colab
- [ ] Testar localmente (se necessário)

---

## 🚀 Alternativa: Versão Colab-Only

Se você **só vai usar Colab**, pode simplificar:

1. **Substituir todos os `BASE_DIR = Path("../")` por:**
   ```python
   BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
   ```

2. **Adicionar no início de cada notebook:**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **Ajustar batch sizes para valores maiores (T4 tem 16GB)**

---

## 📋 Resumo

**O que falta fazer:**

1. ✅ Documentação criada
2. ✅ Notebooks criados
3. ⚠️ **Adaptar caminhos nos notebooks para Colab** (fazer manualmente ou usar detecção automática)
4. ✅ Setup do Colab criado
5. ✅ Requirements.txt criado

**Recomendação:** Use a célula de detecção automática acima - ela funciona tanto no Colab quanto localmente!

