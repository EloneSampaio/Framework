# 📊 Guia de Uso do MLflow

## Instalação

```bash
pip install mlflow
```

## Configuração

O MLflow está configurado para salvar os experimentos em `../mlruns/` (relativo aos notebooks).

## Funcionalidades Integradas

### 1. Rastreamento de Experimentos de Classificação

Cada execução de classificação (SVM ou SRC) para cada braço experimental é automaticamente rastreada no MLflow com:

- **Parâmetros:**
  - Nome do braço experimental
  - Tipo de classificador
  - Hiperparâmetros do modelo
  - Dimensões dos dados

- **Métricas:**
  - Acurácia (validação e teste)
  - F1-Score macro (validação e teste)
  - Silhouette Score

- **Artefatos:**
  - Modelo treinado
  - Scaler usado
  - Classification report
  - Dicionários (para SRC)

### 2. Rastreamento de Análise Estatística

As análises estatísticas são rastreadas com:

- **Parâmetros:**
  - Nível de significância (alpha)
  - Número de braços comparados
  - Resultado do teste de Friedman

- **Métricas:**
  - p-valor do teste de Friedman
  - Estatística de Friedman

- **Artefatos:**
  - Resultados dos pós-testes (Nemenyi, Conover)
  - Visualizações (rankings, heatmaps, CD diagrams)

## Visualizando Resultados

### Iniciar o MLflow UI

```bash
# No diretório raiz do projeto
cd /media/sam/Arquivos/Mestrado/TCC/Framework
mlflow ui
```

Ou especificando o diretório:

```bash
mlflow ui --backend-store-uri ./mlruns
```

### Acessar a Interface Web

Abra seu navegador em: `http://localhost:5000`

## Estrutura de Experimentos

Os experimentos são organizados da seguinte forma:

```
MLflow Experiments:
├── Classification_baseline_cnn_SVM
├── Classification_baseline_cnn_SRC
├── Classification_vit_pure_SVM
├── Classification_vit_pure_SRC
├── Classification_vit_contrastive_SVM
├── Classification_vit_contrastive_SRC
├── Classification_vit_mim_SVM
├── Classification_vit_mim_SRC
├── Classification_vit_sparse_SVM
├── Classification_vit_sparse_SRC
├── Statistical_Analysis_SVM
└── Statistical_Analysis_SRC
```

## Comparando Experimentos

No MLflow UI, você pode:

1. **Comparar Runs:** Selecione múltiplos runs para comparar métricas lado a lado
2. **Filtrar:** Use filtros para encontrar experimentos específicos
3. **Ordenar:** Ordene por qualquer métrica (ex: test_f1_macro)
4. **Visualizar:** Veja gráficos de evolução das métricas ao longo do tempo

## Exportando Resultados

### Exportar para CSV

```python
import mlflow
import pandas as pd

# Conectar ao tracking
mlflow.set_tracking_uri("./mlruns")

# Buscar todos os runs de um experimento
experiment = mlflow.get_experiment_by_name("Classification_vit_pure_SVM")
runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

# Exportar para CSV
runs.to_csv("mlflow_results.csv", index=False)
```

### Comparar Melhores Modelos

```python
import mlflow

# Buscar melhor run por F1-score
experiments = mlflow.search_experiments()
best_runs = []

for exp in experiments:
    runs = mlflow.search_runs(experiment_ids=[exp.experiment_id])
    if len(runs) > 0:
        best_run = runs.loc[runs['metrics.test_f1_macro'].idxmax()]
        best_runs.append(best_run)

# Criar DataFrame comparativo
comparison_df = pd.DataFrame(best_runs)
print(comparison_df[['tags.mlflow.runName', 'metrics.test_f1_macro', 'metrics.test_accuracy']])
```

## Registro de Modelos (Opcional)

Para registrar modelos para produção:

```python
# No notebook de classificação, após treinar o modelo
mlflow.sklearn.log_model(best_svm, "model", registered_model_name=f"{arm_name}_SVM")
```

Depois, você pode carregar o modelo:

```python
import mlflow

# Carregar modelo registrado
model = mlflow.sklearn.load_model(f"models:/{arm_name}_SVM/Production")
```

## Dicas

1. **Tags:** Adicione tags para organizar melhor:
   ```python
   mlflow.set_tag("dataset", "ACDC")
   mlflow.set_tag("version", "1.0")
   ```

2. **Notas:** Adicione notas descritivas aos runs:
   ```python
   mlflow.set_tag("mlflow.note.content", "Primeira execução com dados completos")
   ```

3. **Parâmetros de Sistema:** O MLflow automaticamente registra:
   - Versão do Python
   - Versões das bibliotecas
   - Informações do sistema

## Troubleshooting

### Erro: "No active run"

Certifique-se de que está dentro de um contexto `mlflow.start_run()`:

```python
with mlflow.start_run():
    # seu código aqui
```

### Erro: "Experiment does not exist"

O MLflow cria experimentos automaticamente. Se necessário, crie manualmente:

```python
mlflow.create_experiment("Nome_do_Experimento")
mlflow.set_experiment("Nome_do_Experimento")
```

### Limpar Experimentos Antigos

```python
import shutil
shutil.rmtree("./mlruns")  # Cuidado: remove todos os experimentos!
```

## Recursos Adicionais

- [Documentação oficial do MLflow](https://www.mlflow.org/docs/latest/index.html)
- [MLflow Tracking Guide](https://www.mlflow.org/docs/latest/tracking.html)
- [MLflow UI Guide](https://www.mlflow.org/docs/latest/tracking.html#tracking-ui)

