# 📋 Plano de Adaptação do Pipeline

## Objetivo
Adaptar os notebooks existentes na pasta `scripts/` para seguir o pipeline completo descrito no `README.md`, implementando os 5 braços experimentais e integrando os repositórios de referência.

---

## 🎯 Braços Experimentais a Implementar

1. **Baseline CNN:** U-Net ou ResNet padrão (método clássico)
2. **ViT Puro:** ViT pré-treinado no ImageNet, usado diretamente no dataset médico
3. **ViT + Contrastive (domain_specific_cl):** Usando lógica de perdas globais/locais
4. **ViT + MIM (MIM-Med3D):** Usando lógica de reconstrução por máscara
5. **ViT + Sparse + Classificador:** Aplicação de esparsidade nas representações antes da classificação final

---

## 📊 Datasets a Utilizar

- **ACDC (Coração):** Para o método Contrastivo
- **BraTS (Cérebro) ou BTCV (Órgãos):** Para o método MIM

---

## 🔄 Estrutura do Pipeline Adaptado

### Etapa 1: Download e Preparação de Datasets
**Notebook:** `01_Download_Datasets.ipynb` (NOVO)
- Download do dataset ACDC
- Download do dataset BraTS (ou BTCV)
- Preparação e organização dos dados
- Divisão em train/validation/test

### Etapa 2: Extração de Features
**Notebook:** `02_Feature_Extraction.ipynb` (ADAPTADO de `ExtractorDataset.ipynb`)
- Extração para Baseline CNN (ResNet/U-Net)
- Extração para ViT Puro (ImageNet pré-treinado)
- Extração para ViT + Contrastive (integração com domain_specific_cl)
- Extração para ViT + MIM (integração com MIM-Med3D)
- Extração para ViT + Sparse (aplicação de esparsidade)

### Etapa 3: Classificação
**Notebook:** `03_Classification.ipynb` (ADAPTADO de `SVMClassifier.ipynb` e `SRCClassifier.ipynb`)
- Treinamento de classificadores para cada um dos 5 braços
- Métricas: Acurácia, F1, Silhouette
- Comparação entre SVM e SRC

### Etapa 4: Avaliação Estatística
**Notebook:** `04_Avaliacao_Estatistica.ipynb` (ADAPTADO de `Avaliação_estatitisca.ipynb`)
- Teste de Friedman para os 5 braços
- Pós-testes (Nemenyi, Conover, Bonferroni)
- Visualizações comparativas

### Etapa 5: Visualização e XAI (Opcional)
**Notebook:** `05_Visualizacao_XAI.ipynb` (NOVO)
- Mapas de atenção para os 3 tipos de ViT
- t-SNE para visualização de clusters
- Comparação de representações esparsas vs. outras

---

## 🔧 Integrações Necessárias

### Repositório 1: domain_specific_cl
- **URL:** https://github.com/krishnabits001/domain_specific_cl
- **Uso:** Extrair features usando o modelo contrastivo pré-treinado
- **Método:** Clonar repositório e usar modelo para extração de features

### Repositório 2: MIM-Med3D
- **URL:** https://github.com/chenz53/MIM-Med3D
- **Uso:** Extrair features usando o modelo MIM pré-treinado
- **Método:** Clonar repositório e usar modelo para extração de features

---

## 📁 Estrutura de Diretórios Proposta

```
Framework/
├── README.md
├── REPOSITORIOS.md
├── PLANO_ADAPTACAO.md
├── scripts/
│   ├── 01_Download_Datasets.ipynb
│   ├── 02_Feature_Extraction.ipynb
│   ├── 03_Classification.ipynb
│   ├── 04_Avaliacao_Estatistica.ipynb
│   ├── 05_Visualizacao_XAI.ipynb
│   └── utils/  # Funções auxiliares compartilhadas
├── data/
│   ├── ACDC/
│   ├── BraTS/
│   └── processed/
├── models/
│   ├── baseline_cnn/
│   ├── vit_pure/
│   ├── vit_contrastive/
│   ├── vit_mim/
│   └── vit_sparse/
├── features/
│   ├── baseline_cnn/
│   ├── vit_pure/
│   ├── vit_contrastive/
│   ├── vit_mim/
│   └── vit_sparse/
└── results/
    ├── classifications/
    ├── evaluations/
    └── visualizations/
```

---

## 🚀 Próximos Passos

1. ✅ Criar documento de planejamento
2. ⏳ Criar notebook de download de datasets
3. ⏳ Adaptar notebook de extração de features
4. ⏳ Adaptar notebooks de classificação
5. ⏳ Adaptar notebook de avaliação estatística
6. ⏳ Criar notebook de visualização (opcional)

---

## 📝 Notas Importantes

- Todos os notebooks devem ser modulares e reutilizáveis
- Salvar resultados intermediários para evitar reprocessamento
- Documentar parâmetros e configurações em cada notebook
- Garantir compatibilidade entre etapas do pipeline

