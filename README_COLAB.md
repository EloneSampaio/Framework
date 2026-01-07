# 🚀 Guia Rápido - Execução no Google Colab

## ⚡ Início Rápido (5 minutos)

### 1. Preparar Google Drive

```
Meu Drive/
└── Mestrado_TCC/
    ├── Framework/
    │   └── scripts/  (upload dos notebooks)
    └── datasets/     (upload dos datasets)
```

### 2. Abrir Colab e Configurar

1. Acesse: https://colab.research.google.com/
2. **Runtime > Change runtime type > GPU**
3. Faça upload de `00_Colab_Setup.ipynb`
4. Execute todas as células

### 3. Executar Pipeline

Execute os notebooks na ordem:
1. `00_Colab_Setup.ipynb` ✅ (já executado)
2. `01_Download_Datasets.ipynb`
3. `02_Feature_Extraction.ipynb`
4. `03_Classification.ipynb`
5. `04_Avaliacao_Estatistica.ipynb`

---

## ✅ O que foi adaptado

- ✅ **Detecção automática** de ambiente (Colab vs Local)
- ✅ **Caminhos ajustados** automaticamente
- ✅ **Batch sizes otimizados** para T4 (16GB)
- ✅ **MLflow configurado** para salvar no Drive
- ✅ **Setup completo** no notebook 00

---

## 📊 Batch Sizes no Colab

- Baseline CNN: **64** (vs 32 local)
- ViT Puro: **32** (vs 16 local)
- ViT + Contrastive: **16** (vs 8 local)
- ViT + MIM: **8** (vs 4 local)
- ViT + Sparse: **64** (vs 32 local)

**Resultado:** Processamento ~2x mais rápido! 🚀

---

## 📝 Documentação Completa

- **COLAB_SETUP.md** - Guia detalhado
- **COLAB_QUICK_START.md** - Início rápido
- **ADAPTACAO_COLAB.md** - Detalhes de adaptação
- **CHECKLIST_FINAL.md** - Checklist completo

---

## 🎯 Pronto para Executar!

Tudo está configurado e adaptado para o Colab. Basta seguir os passos acima! 🚀

