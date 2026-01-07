# 📝 Instruções para Adaptação dos Notebooks

## ✅ O que já foi criado

1. **PLANO_ADAPTACAO.md** - Plano completo do pipeline adaptado
2. **01_Download_Datasets.ipynb** - Notebook para download e preparação dos datasets
3. **02_Feature_Extraction.ipynb** - Notebook base para extração de features (estrutura inicial criada)

## 🔧 Próximos Passos

### 1. Completar o Notebook 02_Feature_Extraction.ipynb

Você precisa adicionar as seguintes células ao notebook:

#### Célula: Funções para carregar dados médicos
```python
import nibabel as nib

def load_medical_image(filepath, normalize=True):
    """Carrega imagem médica (2D slice de volume 3D ou imagem 2D)."""
    filepath = Path(filepath)
    
    if filepath.suffix == '.gz' or '.nii' in filepath.name:
        img = nib.load(str(filepath))
        data = img.get_fdata()
        if len(data.shape) == 3:
            data = data[:, :, data.shape[2] // 2]  # Slice central
        if normalize:
            data = (data - data.min()) / (data.max() - data.min() + 1e-8) * 255
        if len(data.shape) == 2:
            data = np.stack([data, data, data], axis=-1)
        return tf.cast(data, tf.uint8)
    else:
        image = tf.io.read_file(str(filepath))
        if filepath.suffix.lower() in ['.jpg', '.jpeg']:
            image = tf.image.decode_jpeg(image, channels=3)
        return image
```

#### Célula: Extrator Baseline CNN
```python
def build_baseline_cnn_extractor(input_size=224):
    """Constrói extrator usando ResNet50 pré-treinado."""
    base_model = ResNet50(weights='imagenet', include_top=False, 
                          input_shape=(input_size, input_size, 3))
    base_model.trainable = False
    
    inputs = layers.Input(shape=(input_size, input_size, 3), dtype=tf.float32)
    x = tf.keras.applications.resnet50.preprocess_input(inputs)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    
    return models.Model(inputs=inputs, outputs=x)
```

#### Célula: Integração com domain_specific_cl
```python
def build_vit_contrastive_extractor(repo_path="../repositories/domain_specific_cl"):
    """
    Integra com o repositório domain_specific_cl.
    
    Passos:
    1. Clone o repositório: git clone https://github.com/krishnabits001/domain_specific_cl
    2. Instale as dependências conforme o README do repositório
    3. Carregue o modelo pré-treinado
    4. Adapte esta função para extrair features
    """
    sys.path.append(str(Path(repo_path).absolute()))
    
    # TODO: Adaptar conforme a estrutura do repositório
    # Exemplo:
    # from models import YourContrastiveModel
    # model = YourContrastiveModel.load_from_checkpoint(checkpoint_path)
    # return model
    
    # Por enquanto, fallback para ViT puro
    return build_vit_pure_extractor()
```

#### Célula: Integração com MIM-Med3D
```python
def build_vit_mim_extractor(repo_path="../repositories/MIM-Med3D"):
    """
    Integra com o repositório MIM-Med3D.
    
    Passos:
    1. Clone o repositório: git clone https://github.com/chenz53/MIM-Med3D
    2. Instale as dependências conforme o README do repositório
    3. Carregue o modelo pré-treinado
    4. Adapte esta função para extrair features
    """
    sys.path.append(str(Path(repo_path).absolute()))
    
    # TODO: Adaptar conforme a estrutura do repositório
    # Exemplo:
    # from models import MIMViT
    # model = MIMViT.load_from_checkpoint(checkpoint_path)
    # return model
    
    # Por enquanto, fallback para ViT puro
    return build_vit_pure_extractor()
```

#### Célula: Aplicação de Esparsidade
```python
from sklearn.decomposition import DictionaryLearning

def apply_sparsity_to_features(features, n_atoms=50, alpha=0.1):
    """Aplica esparsidade nas features usando Dictionary Learning."""
    dict_learner = DictionaryLearning(
        n_components=n_atoms,
        alpha=alpha,
        fit_algorithm='lars',
        transform_algorithm='lasso_lars',
        n_jobs=-1
    )
    sparse_features = dict_learner.fit_transform(features)
    return sparse_features, dict_learner
```

### 2. Adaptar o Notebook 03_Classification.ipynb

Baseado nos notebooks `SVMClassifier.ipynb` e `SRCClassifier.ipynb`, criar um notebook que:

1. Carrega features de todos os 5 braços experimentais
2. Treina classificadores (SVM e SRC) para cada braço
3. Calcula métricas (Acurácia, F1, Silhouette) para cada combinação
4. Salva resultados em estrutura organizada

**Estrutura esperada:**
```python
# Para cada braço experimental
for arm in ["baseline_cnn", "vit_pure", "vit_contrastive", "vit_mim", "vit_sparse"]:
    # Carregar features
    train_features = np.load(f"../features/{arm}/train_features.npy")
    train_labels = np.load(f"../features/{arm}/train_labels.npy")
    # ... val e test
    
    # Treinar SVM
    svm_results = train_svm_classifier(train_features, train_labels, ...)
    
    # Treinar SRC
    src_results = train_src_classifier(train_features, train_labels, ...)
    
    # Salvar resultados
    save_results(arm, svm_results, src_results)
```

### 3. Adaptar o Notebook 04_Avaliacao_Estatistica.ipynb

Baseado no notebook `Avaliação_estatitisca.ipynb`, adaptar para:

1. Carregar resultados de todos os 5 braços experimentais
2. Executar Teste de Friedman
3. Executar pós-testes (Nemenyi, Conover, Bonferroni)
4. Gerar visualizações comparativas

**Estrutura esperada:**
```python
# Carregar F1-scores de todos os braços
f1_scores = {
    "Baseline CNN": [...],
    "ViT Puro": [...],
    "ViT + Contrastive": [...],
    "ViT + MIM": [...],
    "ViT + Sparse": [...]
}

# Executar análise estatística
analysis = StatisticalAnalysis(f1_scores, alpha=0.05)
analysis.friedman_test()
analysis.nemenyi_test()
# ... outros testes
```

### 4. Criar Notebook 05_Visualizacao_XAI.ipynb (Opcional)

Este notebook deve:

1. Gerar mapas de atenção para os 3 tipos de ViT
2. Visualizar clusters usando t-SNE
3. Comparar representações esparsas vs. outras

## 🔗 Integração com Repositórios

### Repositório 1: domain_specific_cl

**URL:** https://github.com/krishnabits001/domain_specific_cl

**Passos para integração:**
1. Clone o repositório:
   ```bash
   cd ../repositories
   git clone https://github.com/krishnabits001/domain_specific_cl
   ```

2. Instale dependências conforme o README do repositório

3. Baixe o modelo pré-treinado (se disponível)

4. Adapte a função `build_vit_contrastive_extractor()` para carregar o modelo

5. Use o modelo para extrair features do dataset ACDC

### Repositório 2: MIM-Med3D

**URL:** https://github.com/chenz53/MIM-Med3D

**Passos para integração:**
1. Clone o repositório:
   ```bash
   cd ../repositories
   git clone https://github.com/chenz53/MIM-Med3D
   ```

2. Instale dependências conforme o README do repositório

3. Baixe o modelo pré-treinado (se disponível)

4. Adapte a função `build_vit_mim_extractor()` para carregar o modelo

5. Use o modelo para extrair features do dataset BraTS

## 📊 Estrutura de Dados Esperada

### Features
```
features/
├── baseline_cnn/
│   ├── train_features.npy
│   ├── train_labels.npy
│   ├── val_features.npy
│   ├── val_labels.npy
│   ├── test_features.npy
│   └── test_labels.npy
├── vit_pure/
│   └── ...
├── vit_contrastive/
│   └── ...
├── vit_mim/
│   └── ...
└── vit_sparse/
    └── ...
```

### Resultados
```
results/
├── classifications/
│   ├── baseline_cnn_svm_results.json
│   ├── baseline_cnn_src_results.json
│   └── ...
├── evaluations/
│   ├── friedman_test_results.json
│   └── posthoc_test_results.json
└── visualizations/
    ├── attention_maps/
    └── tsne_plots/
```

## 🚀 Ordem de Execução

1. **01_Download_Datasets.ipynb** - Baixar e preparar datasets
2. **02_Feature_Extraction.ipynb** - Extrair features para todos os braços
3. **03_Classification.ipynb** - Treinar classificadores
4. **04_Avaliacao_Estatistica.ipynb** - Avaliar resultados estatisticamente
5. **05_Visualizacao_XAI.ipynb** (opcional) - Visualizações e XAI

## 📝 Notas Importantes

- Todos os notebooks devem ser modulares e reutilizáveis
- Salvar resultados intermediários para evitar reprocessamento
- Documentar parâmetros e configurações em cada notebook
- Garantir compatibilidade entre etapas do pipeline
- Adaptar funções de carregamento de dados para cada dataset específico (ACDC vs BraTS)

## 🔍 Verificação

Após completar a adaptação, verifique:

- [ ] Todos os 5 braços experimentais estão implementados
- [ ] Features são extraídas corretamente para cada braço
- [ ] Classificadores são treinados para todos os braços
- [ ] Avaliação estatística compara todos os braços
- [ ] Resultados são salvos em estrutura organizada
- [ ] Integração com repositórios externos funciona

