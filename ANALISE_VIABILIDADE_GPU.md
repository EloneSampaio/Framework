# 🖥️ Análise de Viabilidade - GPU RTX 3050 6GB

## Especificações do Sistema

### GPU
- **Modelo:** NVIDIA GeForce RTX 3050 6GB Laptop GPU
- **Memória VRAM:** 6 GB (6144 MiB)
- **Compute Capability:** 8.6 (Arquitetura Ampere)
- **Driver:** 535.274.02

### Sistema
- **RAM:** 21 GB total (~5 GB disponível)
- **CPU:** 12 cores
- **Swap:** 5.6 GB

---

## ✅ Análise por Componente do Pipeline

### 1. **Download e Preparação de Datasets** ✅
**Viabilidade:** ✅ **SIM - Sem problemas**

- Não requer GPU
- Operações de I/O e descompactação
- RAM suficiente para processar arquivos

**Recomendações:**
- Processar datasets em lotes se necessário
- Usar links simbólicos para economizar espaço em disco

---

### 2. **Extração de Features** ⚠️
**Viabilidade:** ⚠️ **SIM, mas com limitações**

#### 2.1 Baseline CNN (ResNet50) ✅
- **Memória necessária:** ~2-3 GB VRAM
- **Batch size recomendado:** 16-32
- **Status:** ✅ Funciona bem

#### 2.2 ViT Puro ✅
- **Memória necessária:** ~2-4 GB VRAM
- **Batch size recomendado:** 8-16 (dependendo do modelo)
- **Status:** ✅ Funciona, mas com batches menores

#### 2.3 ViT + Contrastive (domain_specific_cl) ⚠️
- **Memória necessária:** ~3-5 GB VRAM
- **Batch size recomendado:** 4-8
- **Status:** ⚠️ Funciona, mas pode ser lento
- **Nota:** Usa TensorFlow 1.x (pode ter problemas de compatibilidade)

#### 2.4 ViT + MIM (MIM-Med3D) ⚠️
- **Memória necessária:** ~4-6 GB VRAM
- **Batch size recomendado:** 2-4 (dados 3D são pesados)
- **Status:** ⚠️ **Limite da GPU - requer otimizações**
- **Dados 3D:** Volumes médicos são muito pesados para 6GB

#### 2.5 ViT + Sparse ✅
- **Memória necessária:** ~1-2 GB VRAM (apenas processamento CPU)
- **Status:** ✅ Funciona sem problemas

**Recomendações para Extração:**
```python
# Ajustar batch sizes no notebook 02_Feature_Extraction.ipynb
BATCH_SIZES = {
    "baseline_cnn": 32,
    "vit_pure": 16,
    "vit_contrastive": 8,
    "vit_mim": 4,  # Reduzido para dados 3D
    "vit_sparse": 32
}
```

---

### 3. **Classificação (SVM e SRC)** ✅
**Viabilidade:** ✅ **SIM - Sem problemas**

- **SVM:** Executa principalmente na CPU
- **SRC:** Executa principalmente na CPU
- **Memória RAM:** Suficiente para datasets médios

**Recomendações:**
- Usar `n_jobs=-1` para paralelizar no CPU
- Processar em chunks se o dataset for muito grande

---

### 4. **Avaliação Estatística** ✅
**Viabilidade:** ✅ **SIM - Sem problemas**

- Operações estatísticas na CPU
- Visualizações leves
- Sem requisitos de GPU

---

## 🎯 Resumo de Viabilidade

| Componente | Viabilidade | Batch Size Recomendado | Observações |
|-----------|-------------|----------------------|-------------|
| Download Datasets | ✅ Excelente | N/A | Sem GPU necessária |
| Baseline CNN | ✅ Boa | 32 | Funciona bem |
| ViT Puro | ✅ Boa | 16 | Funciona bem |
| ViT + Contrastive | ⚠️ Moderada | 8 | Pode ser lento |
| ViT + MIM | ⚠️ **Limitada** | **2-4** | **Limite da GPU** |
| ViT + Sparse | ✅ Excelente | 32 | CPU apenas |
| Classificação | ✅ Excelente | N/A | CPU apenas |
| Avaliação Estatística | ✅ Excelente | N/A | CPU apenas |

---

## ⚠️ Principais Desafios

### 1. **Memória VRAM Limitada (6GB)**
- **Problema:** Dados médicos 3D (BraTS, ACDC) são volumosos
- **Solução:** 
  - Reduzir batch size para 2-4
  - Processar volumes em slices 2D
  - Usar mixed precision (já implementado)

### 2. **ViT + MIM (Dados 3D)**
- **Problema:** Modelos 3D consomem muita memória
- **Solução:**
  - Processar apenas slices 2D dos volumes
  - Usar gradient checkpointing se disponível
  - Considerar usar apenas dados 2D para este braço

### 3. **domain_specific_cl (TensorFlow 1.x)**
- **Problema:** Incompatibilidade com versões modernas
- **Solução:**
  - Usar ambiente virtual separado
  - Ou usar fallback para ViT puro (já implementado)

---

## 🚀 Otimizações Recomendadas

### 1. **Mixed Precision** ✅ (Já implementado)
```python
# Já está no código
policy = tf.keras.mixed_precision.Policy('mixed_float16')
```

### 2. **Processamento em Slices 2D**
Para dados 3D, processar slice por slice:
```python
# Em vez de processar volume completo
for slice_idx in range(volume.shape[2]):
    slice_2d = volume[:, :, slice_idx]
    features = extract_features(slice_2d)
```

### 3. **Gradient Checkpointing**
Para modelos grandes:
```python
# Se disponível no modelo
model.gradient_checkpointing = True
```

### 4. **Limpar Cache da GPU**
```python
import torch
torch.cuda.empty_cache()  # PyTorch
# ou
tf.keras.backend.clear_session()  # TensorFlow
```

### 5. **Monitorar Uso de Memória**
```python
# Adicionar ao notebook
import GPUtil
gpus = GPUtil.getGPUs()
for gpu in gpus:
    print(f"GPU {gpu.id}: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB")
```

---

## 📊 Estimativa de Tempo de Execução

### Com otimizações:
- **Download Datasets:** 1-2 horas (depende da conexão)
- **Extração Baseline CNN:** 2-4 horas
- **Extração ViT Puro:** 3-6 horas
- **Extração ViT + Contrastive:** 4-8 horas
- **Extração ViT + MIM:** **8-16 horas** (mais lento devido a batch size pequeno)
- **Extração ViT + Sparse:** 1-2 horas
- **Classificação:** 1-3 horas
- **Avaliação Estatística:** 10-30 minutos

**Total estimado:** ~20-40 horas (pode ser executado em paralelo onde possível)

---

## ✅ Conclusão

### **SIM, sua GPU consegue executar o pipeline!**

**Mas com as seguintes ressalvas:**

1. ✅ **Maioria dos componentes:** Funciona bem
2. ⚠️ **ViT + MIM:** Requer batch size muito pequeno (2-4)
3. ⚠️ **Processamento será mais lento** do que em GPUs maiores
4. ✅ **Classificação e análise:** Sem problemas

### Recomendações Finais:

1. **Comece pelos braços mais leves:**
   - Baseline CNN
   - ViT Puro
   - ViT + Sparse

2. **Deixe ViT + MIM por último** e considere:
   - Processar apenas slices 2D
   - Ou usar dataset 2D alternativo

3. **Monitore o uso de memória** durante a execução

4. **Use o MLflow** para rastrear o progresso e não perder resultados

5. **Execute em etapas:** Não tente processar tudo de uma vez

---

## 🔧 Script de Monitoramento

Adicione este código aos notebooks para monitorar:

```python
def monitor_gpu():
    """Monitora uso da GPU durante execução."""
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            print(f"GPU {gpu.name}:")
            print(f"  Memória: {gpu.memoryUsed}MB / {gpu.memoryTotal}MB ({gpu.memoryUtil*100:.1f}%)")
            print(f"  Carga: {gpu.load*100:.1f}%")
    except ImportError:
        print("GPUtil não instalado. Instale com: pip install GPUtil")
    except Exception as e:
        print(f"Erro ao monitorar GPU: {e}")

# Chamar periodicamente
monitor_gpu()
```

---

## 📝 Checklist de Preparação

Antes de executar:

- [ ] Instalar todas as dependências
- [ ] Verificar espaço em disco (datasets são grandes)
- [ ] Configurar batch sizes apropriados
- [ ] Preparar ambiente para TensorFlow 1.x (se usar domain_specific_cl)
- [ ] Configurar swap se necessário
- [ ] Iniciar MLflow UI para monitoramento
- [ ] Fazer backup dos resultados periodicamente

**Boa sorte com a execução! 🚀**

