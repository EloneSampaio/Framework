# 🚀 Guia de Configuração para Google Colab

## Por que usar Colab?

- ✅ **GPUs gratuitas:** T4 (16GB), V100 (16GB), ou A100 (40GB)
- ✅ **Mais memória:** Sem limitações de hardware local
- ✅ **Execução longa:** Pode deixar rodando por horas
- ✅ **Fácil compartilhamento:** Compartilhe notebooks facilmente

---

## 📋 Pré-requisitos

1. Conta Google
2. Google Drive com espaço suficiente (~50-100GB recomendado)
3. Acesso ao Colab: https://colab.research.google.com/

---

## 🔧 Passo 1: Preparar Google Drive

### 1.1 Estrutura de Pastas no Drive

Crie a seguinte estrutura no seu Google Drive:

```
Meu Drive/
└── Mestrado_TCC/
    ├── Framework/          # Upload dos notebooks
    ├── datasets/          # Datasets (ACDC, BraTS)
    ├── repositories/      # Repositórios clonados
    ├── features/          # Features extraídas (será criado)
    ├── results/           # Resultados (será criado)
    └── mlruns/            # MLflow (será criado)
```

### 1.2 Upload dos Arquivos

1. **Upload dos notebooks:**
   - Faça upload da pasta `scripts/` para `Mestrado_TCC/Framework/scripts/`

2. **Upload dos datasets:**
   - Faça upload dos datasets ACDC e BraTS para `Mestrado_TCC/datasets/`

3. **Upload dos repositórios (opcional):**
   - Ou clone diretamente no Colab

---

## 🔧 Passo 2: Configuração Inicial no Colab

### 2.1 Célula de Setup Inicial

Adicione esta célula no início de cada notebook:

```python
# ============================================
# CONFIGURAÇÃO INICIAL PARA GOOGLE COLAB
# ============================================

import os
from pathlib import Path

# Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Configurar caminhos
BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
FRAMEWORK_DIR = BASE_DIR / "Framework"
DATA_DIR = BASE_DIR / "datasets"
REPOS_DIR = BASE_DIR / "repositories"
FEATURES_DIR = BASE_DIR / "features"
RESULTS_DIR = BASE_DIR / "results"
MLRUNS_DIR = BASE_DIR / "mlruns"

# Criar diretórios se não existirem
for dir_path in [FEATURES_DIR, RESULTS_DIR, MLRUNS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Mudar para diretório do framework
os.chdir(FRAMEWORK_DIR)

print("✅ Google Drive montado!")
print(f"📁 Diretório base: {BASE_DIR}")
print(f"📁 Framework: {FRAMEWORK_DIR}")
```

### 2.2 Verificar GPU

```python
# Verificar GPU disponível
import tensorflow as tf

print("🔍 Verificando GPU...")
print(f"GPUs disponíveis: {len(tf.config.list_physical_devices('GPU'))}")

if tf.config.list_physical_devices('GPU'):
    gpu = tf.config.list_physical_devices('GPU')[0]
    print(f"✅ GPU detectada: {gpu}")
    
    # Configurar memória GPU
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            # Permitir crescimento de memória
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print("✅ Memória GPU configurada para crescimento dinâmico")
        except RuntimeError as e:
            print(f"⚠️  Erro ao configurar GPU: {e}")
else:
    print("⚠️  Nenhuma GPU detectada. Verifique Runtime > Change runtime type > GPU")
```

---

## 🔧 Passo 3: Instalar Dependências

### 3.1 Célula de Instalação

Adicione no início de cada notebook:

```python
# ============================================
# INSTALAÇÃO DE DEPENDÊNCIAS
# ============================================

!pip install -q mlflow
!pip install -q scikit-posthocs
!pip install -q nibabel
!pip install -q transformers
!pip install -q tensorflow
!pip install -q scikit-learn
!pip install -q pandas
!pip install -q numpy
!pip install -q matplotlib
!pip install -q seaborn

# Para monitoramento (opcional)
!pip install -q GPUtil

print("✅ Dependências instaladas!")
```

### 3.2 Instalar Repositórios (se necessário)

```python
# Clonar repositórios diretamente no Colab
import os

REPOS_DIR = Path("/content/drive/MyDrive/Mestrado_TCC/repositories")
REPOS_DIR.mkdir(parents=True, exist_ok=True)

# Clonar domain_specific_cl
if not (REPOS_DIR / "domain_specific_cl").exists():
    !cd {REPOS_DIR} && git clone https://github.com/krishnabits001/domain_specific_cl

# Clonar MIM-Med3D
if not (REPOS_DIR / "MIM-Med3D").exists():
    !cd {REPOS_DIR} && git clone https://github.com/chenz53/MIM-Med3D

print("✅ Repositórios clonados!")
```

---

## 📝 Adaptações Necessárias nos Notebooks

### 4.1 Notebook 01_Download_Datasets.ipynb

**Mudanças:**
- Caminhos apontam para `/content/drive/MyDrive/...`
- Usar `!wget` ou `!gdown` para downloads diretos (se links disponíveis)

```python
# Exemplo de download direto no Colab
# !gdown --id SEU_FILE_ID --output /content/drive/MyDrive/Mestrado_TCC/datasets/
```

### 4.2 Notebook 02_Feature_Extraction.ipynb

**Mudanças:**
- Ajustar `BASE_DIR` para usar caminhos do Drive
- Batch sizes podem ser maiores (T4 tem 16GB)
- Adicionar verificação de GPU

```python
# Configuração de diretórios (adaptado para Colab)
BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
DATA_DIR = BASE_DIR / "datasets" / "processed"
FEATURES_DIR = BASE_DIR / "features"

# Batch sizes otimizados para Colab T4 (16GB)
BATCH_SIZES = {
    "baseline_cnn": 64,      # Aumentado
    "vit_pure": 32,          # Aumentado
    "vit_contrastive": 16,   # Aumentado
    "vit_mim": 8,            # Aumentado (ainda limitado por dados 3D)
    "vit_sparse": 64
}
```

### 4.3 Notebook 03_Classification.ipynb

**Mudanças:**
- Ajustar caminhos para Drive
- MLflow aponta para Drive

```python
# Configuração MLflow para Colab
MLFLOW_TRACKING_URI = Path("/content/drive/MyDrive/Mestrado_TCC/mlruns")
mlflow.set_tracking_uri(str(MLFLOW_TRACKING_URI.absolute()))
```

### 4.4 Notebook 04_Avaliacao_Estatistica.ipynb

**Mudanças:**
- Ajustar caminhos para Drive
- MLflow aponta para Drive

---

## 🚀 Execução no Colab

### 5.1 Ordem de Execução

1. **01_Download_Datasets.ipynb**
   - Upload do notebook para Colab
   - Executar células na ordem
   - Verificar se datasets foram salvos no Drive

2. **02_Feature_Extraction.ipynb**
   - Executar para cada braço experimental
   - Monitorar uso de GPU
   - Features serão salvas no Drive

3. **03_Classification.ipynb**
   - Executar pipeline completo
   - Resultados salvos no Drive

4. **04_Avaliacao_Estatistica.ipynb**
   - Executar análise estatística
   - Visualizações salvas no Drive

### 5.2 Dicas de Execução

**Para sessões longas:**
```python
# Prevenir timeout (executar periodicamente)
import time
while True:
    time.sleep(300)  # 5 minutos
    print("⏰ Keep-alive: ainda rodando...")
```

**Salvar progresso:**
```python
# Salvar checkpoint periódico
import pickle

checkpoint = {
    'processed_files': processed_files,
    'current_batch': current_batch,
    'features': features_so_far
}

with open('/content/drive/MyDrive/Mestrado_TCC/checkpoint.pkl', 'wb') as f:
    pickle.dump(checkpoint, f)
```

**Monitorar GPU:**
```python
# Em célula separada, executar periodicamente
!nvidia-smi
```

---

## 📊 Vantagens do Colab

### GPU T4 (Gratuita)
- **16GB VRAM** (vs 6GB local)
- **Batch sizes maiores:** 2-4x mais rápido
- **Sem limitações de memória local**

### GPU V100/A100 (Colab Pro)
- **Ainda mais potente**
- **Processamento muito mais rápido**

---

## ⚠️ Limitações do Colab

1. **Timeout:** Sessões gratuitas têm timeout de ~12 horas
   - **Solução:** Salvar checkpoints e continuar depois

2. **Limite de uso:** Pode ter limites de uso de GPU
   - **Solução:** Colab Pro remove limites

3. **Velocidade de upload/download:** Depende da conexão
   - **Solução:** Usar datasets já no Drive

---

## 🔄 Sincronização com Local

### Baixar Resultados

```python
# No final de cada notebook, compactar resultados
!cd /content/drive/MyDrive/Mestrado_TCC && zip -r results_backup.zip results/ features/ mlruns/
```

Depois baixe do Drive para sua máquina local.

---

## 📝 Checklist de Setup

- [ ] Criar estrutura de pastas no Google Drive
- [ ] Upload dos notebooks para Drive
- [ ] Upload dos datasets (ou preparar para download)
- [ ] Configurar primeiro notebook com células de setup
- [ ] Verificar GPU disponível no Colab
- [ ] Testar execução de um braço experimental
- [ ] Configurar MLflow para salvar no Drive
- [ ] Configurar checkpoints periódicos

---

## 🎯 Próximos Passos

1. **Adaptar notebooks:** Adicionar células de setup no início
2. **Testar:** Executar um braço experimental completo
3. **Otimizar:** Ajustar batch sizes para GPU do Colab
4. **Monitorar:** Acompanhar uso de recursos

**Boa execução no Colab! 🚀**

