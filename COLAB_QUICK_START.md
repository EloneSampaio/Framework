# ⚡ Quick Start - Google Colab

## 🚀 Início Rápido (5 minutos)

### 1. Preparar Google Drive

Crie esta estrutura no seu Google Drive:
```
Meu Drive/
└── Mestrado_TCC/
    ├── Framework/
    │   └── scripts/  (faça upload dos notebooks aqui)
    └── datasets/     (faça upload dos datasets aqui)
```

### 2. Abrir Colab

1. Acesse: https://colab.research.google.com/
2. **File > Upload notebook**
3. Faça upload de `00_Colab_Setup.ipynb`

### 3. Configurar GPU

1. **Runtime > Change runtime type**
2. Selecione **GPU** (T4, V100 ou A100)
3. Clique **Save**

### 4. Executar Setup

Execute todas as células do `00_Colab_Setup.ipynb` na ordem.

### 5. Executar Pipeline

Execute os notebooks na ordem:
1. `01_Download_Datasets.ipynb`
2. `02_Feature_Extraction.ipynb`
3. `03_Classification.ipynb`
4. `04_Avaliacao_Estatistica.ipynb`

---

## 📝 Célula de Setup Rápido

Copie e cole esta célula no início de cada notebook:

```python
# Setup rápido para Colab
from google.colab import drive
from pathlib import Path
import os

# Montar Drive
drive.mount('/content/drive')

# Configurar caminhos
BASE_DIR = Path("/content/drive/MyDrive/Mestrado_TCC")
os.chdir(BASE_DIR / "Framework")

# Verificar GPU
import tensorflow as tf
print(f"GPU: {len(tf.config.list_physical_devices('GPU'))} disponível")
```

---

## ⚙️ Batch Sizes para Colab

```python
# Otimizado para T4 (16GB)
BATCH_SIZES = {
    "baseline_cnn": 64,
    "vit_pure": 32,
    "vit_contrastive": 16,
    "vit_mim": 8,
    "vit_sparse": 64
}
```

---

## 🔍 Monitoramento

```python
# Ver uso de GPU
!nvidia-smi

# Ver espaço no Drive
!df -h /content/drive/MyDrive
```

---

## 💾 Salvar Checkpoints

```python
# Salvar progresso periodicamente
import pickle

checkpoint = {'status': 'running', 'progress': 50}
with open('/content/drive/MyDrive/Mestrado_TCC/checkpoint.pkl', 'wb') as f:
    pickle.dump(checkpoint, f)
```

---

## 🎯 Pronto!

Agora é só executar os notebooks na ordem. Tudo será salvo automaticamente no Google Drive!

