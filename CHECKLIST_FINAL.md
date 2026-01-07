# ✅ Checklist Final - Pipeline Completo

## 📋 Antes de Começar

### Documentação
- [x] README.md - Visão geral do projeto
- [x] PLANO_ADAPTACAO.md - Plano detalhado
- [x] INSTRUCOES_ADAPTACAO.md - Instruções de adaptação
- [x] RESUMO_ADAPTACAO.md - Resumo do trabalho
- [x] COLAB_SETUP.md - Guia para Colab
- [x] COLAB_QUICK_START.md - Início rápido
- [x] MLFLOW_GUIDE.md - Guia do MLflow
- [x] ANALISE_VIABILIDADE_GPU.md - Análise de hardware
- [x] REPOSITORIOS.md - Links dos repositórios
- [x] requirements.txt - Dependências

### Notebooks
- [x] 00_Colab_Setup.ipynb - Setup inicial para Colab
- [x] 01_Download_Datasets.ipynb - Download de datasets
- [x] 02_Feature_Extraction.ipynb - Extração de features
- [x] 03_Classification.ipynb - Classificação
- [x] 04_Avaliacao_Estatistica.ipynb - Análise estatística

### Scripts e Utilitários
- [x] scripts/colab_setup.py - Script de setup
- [x] scripts/utils/gpu_monitor.py - Monitoramento de GPU

### Repositórios
- [x] repositories/domain_specific_cl/ - Clonado
- [x] repositories/MIM-Med3D/ - Clonado

---

## 🚀 Preparação para Execução no Colab

### 1. Preparar Google Drive
- [ ] Criar pasta `Mestrado_TCC` no Google Drive
- [ ] Criar subpastas:
  - [ ] `Framework/scripts/` - Para notebooks
  - [ ] `datasets/` - Para datasets
  - [ ] `repositories/` - Para repositórios (ou clonar no Colab)
- [ ] Fazer upload dos notebooks para `Framework/scripts/`
- [ ] Fazer upload dos datasets (ou preparar links de download)

### 2. Configurar Colab
- [ ] Acessar https://colab.research.google.com/
- [ ] Fazer upload de `00_Colab_Setup.ipynb`
- [ ] Configurar Runtime: Runtime > Change runtime type > GPU
- [ ] Executar `00_Colab_Setup.ipynb` completamente

### 3. Verificar Ambiente
- [ ] GPU detectada e funcionando
- [ ] Google Drive montado
- [ ] Dependências instaladas
- [ ] Repositórios clonados (se necessário)
- [ ] Estrutura de diretórios criada

---

## 📝 Execução do Pipeline

### Etapa 1: Download de Datasets
- [ ] Executar `01_Download_Datasets.ipynb`
- [ ] Verificar se datasets foram baixados
- [ ] Verificar se datasets foram organizados corretamente
- [ ] Verificar espaço no Drive

### Etapa 2: Extração de Features
- [ ] Executar `02_Feature_Extraction.ipynb`
- [ ] Para cada braço experimental:
  - [ ] Baseline CNN
  - [ ] ViT Puro
  - [ ] ViT + Contrastive
  - [ ] ViT + MIM
  - [ ] ViT + Sparse
- [ ] Verificar se features foram salvas
- [ ] Verificar shapes das features

### Etapa 3: Classificação
- [ ] Executar `03_Classification.ipynb`
- [ ] Verificar se classificadores foram treinados
- [ ] Verificar se resultados foram salvos
- [ ] Verificar métricas (Acurácia, F1, Silhouette)
- [ ] Verificar MLflow (se habilitado)

### Etapa 4: Avaliação Estatística
- [ ] Executar `04_Avaliacao_Estatistica.ipynb`
- [ ] Verificar teste de Friedman
- [ ] Verificar pós-testes (se aplicável)
- [ ] Verificar visualizações geradas
- [ ] Verificar resultados salvos

---

## 🔍 Validação dos Resultados

### Features
- [ ] Features de todos os 5 braços extraídas
- [ ] Features salvas em formato .npy
- [ ] Labels correspondentes salvos
- [ ] Shapes corretos (n_samples, n_features)

### Classificação
- [ ] Resultados SVM para todos os braços
- [ ] Resultados SRC para todos os braços
- [ ] Tabela resumo gerada
- [ ] Métricas calculadas corretamente

### Análise Estatística
- [ ] Teste de Friedman executado
- [ ] Pós-testes executados (se necessário)
- [ ] Visualizações geradas
- [ ] Resultados exportados

### MLflow
- [ ] Experimentos rastreados
- [ ] Métricas logadas
- [ ] Modelos salvos
- [ ] Artefatos salvos

---

## 📊 Estrutura Final Esperada

```
Google Drive/Mestrado_TCC/
├── Framework/
│   └── scripts/
│       ├── 00_Colab_Setup.ipynb
│       ├── 01_Download_Datasets.ipynb
│       ├── 02_Feature_Extraction.ipynb
│       ├── 03_Classification.ipynb
│       └── 04_Avaliacao_Estatistica.ipynb
├── datasets/
│   ├── ACDC/
│   └── BraTS/
├── repositories/
│   ├── domain_specific_cl/
│   └── MIM-Med3D/
├── features/
│   ├── baseline_cnn/
│   ├── vit_pure/
│   ├── vit_contrastive/
│   ├── vit_mim/
│   └── vit_sparse/
├── results/
│   ├── classifications/
│   └── evaluations/
└── mlruns/
    └── (experimentos do MLflow)
```

---

## ⚠️ Problemas Comuns e Soluções

### GPU não detectada
- **Solução:** Runtime > Change runtime type > GPU

### Timeout da sessão
- **Solução:** Salvar checkpoints periodicamente

### Memória insuficiente
- **Solução:** Reduzir batch size

### Erro ao montar Drive
- **Solução:** Re-executar célula de montagem

### Dependências não instaladas
- **Solução:** Re-executar célula de instalação

---

## 🎯 Próximos Passos Após Execução

1. **Baixar resultados do Drive:**
   - Features extraídas
   - Resultados de classificação
   - Visualizações
   - Logs do MLflow

2. **Analisar resultados:**
   - Comparar métricas entre braços
   - Verificar significância estatística
   - Gerar tabelas finais

3. **Preparar para artigo:**
   - Tabela comparativa dos 5 braços
   - Gráficos de ranking
   - Diagramas de diferença crítica
   - Mapas de atenção (se implementado)

---

## ✅ Status Final

- [ ] Pipeline completo executado
- [ ] Todos os resultados obtidos
- [ ] Análise estatística completa
- [ ] Resultados validados
- [ ] Pronto para escrita do artigo

**Boa execução! 🚀**

