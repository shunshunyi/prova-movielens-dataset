# 4. Guia de Execução

Este guia descreve passo-a-passo como executar o projeto a partir do zero.

## 4.1 Pré-requisitos
Antes de começar, certifique-se de que sua máquina possui:
1.  **Docker Desktop** (com Docker Compose) instalado e rodando.
    *   *Verificação*: `docker --version` e `docker-compose --version`
2.  **Git** (para clonar o repositório).
3.  **(Opcional)** **Python 3.8+** se desejar rodar scripts de ingestão fora do Docker.

## 4.2 Inicialização

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd prova-movielens-dataset
```

### 2. Subir a Infraestrutura
Na raiz do projeto, execute:
```bash
docker-compose -f infra/docker-compose.yml up -d
```
*   **O que isso faz?**
    *   Inicia o Spark Master (Porta 8080 - Web UI).
    *   Inicia o Spark Worker.
    *   Inicia o MinIO (Porta 9001 - Console, 9000 - API).
    *   Cria automaticamente os buckets `raw`, `bronze` e `silver`.
*   **Verificação**:
    *   Acesse `http://localhost:9001` no navegador.
    *   Login: `minioadmin` / Senha: `minioadmin`.
    *   Confirme se os buckets estão vazios.

## 4.3 Ingestão e Processamento

### Passo 1: Ingestão de Dados
Este passo lê os dados da pasta local `datasets/ml-latest-small` e os envia para a camada **Raw**.
1.  Instale as dependências Python (se ainda não tiver):
    ```bash
    pip install -r requirements.txt
    ```
2.  **Verifique se os dados estão presentes**:  
    Certifique-se de que a pasta `datasets/ml-latest-small` contém `movies.csv` e `ratings.csv`.
3.  Execute o script:
    ```bash
    python src/ingest.py
    ```
4.  **Verificação**: Check no MinIO (`http://localhost:9001`), bucket `raw` deve conter `movies.csv` e `ratings.csv`.

### Passo 2: Processamento (Pipeline ETL)
Este passo executa o job Spark que transforma Raw -> Bronze -> Silver.

**Recomendado: Executar via Docker**
Para evitar problemas de configuração de ambiente local (Java/Hadoop), rode o job dentro do container do Spark Master:

```bash
docker exec -u 0 spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.hadoop:hadoop-aws:3.4.1 \
  --master spark://spark-master:7077 \
  /opt/spark/process.py
```

*   **Verificação**: Check no MinIO.
    *   Bucket `bronze`: deve conter pastas `ratings/` e `movies/` com arquivos `.parquet`.
    *   Bucket `silver`: deve conter pastas `movie_ratings/` e `genre_counts/` com arquivos `.parquet`.

## 4.4 Análise e Visualização
1.  Instale as dependências de análise:
    ```bash
    pip install notebook pandas matplotlib s3fs pyarrow
    ```
    *(Nota: `requirements.txt` já inclui estas libs)*
2.  Inicie o Jupyter Notebook:
    ```bash
    jupyter notebook
    ```
3.  Navegue até a pasta `notebooks` e abra `analysis.ipynb`.
4.  Execute todas as células ("Run All") para visualizar os gráficos de "Top 10 Filmes" e "Distribuição de Gêneros".

## 4.5 Troubleshooting

| Problema | Solução Possível |
| :--- | :--- |
| **Connection Refused (MinIO)** | Confirme se o Docker está rodando e se a porta 9000 não está em uso por outro serviço. |
| **Spark: ClassNotFoundException** | Verifique se o comando `docker exec` incluiu a flag `--packages` correta (`hadoop-aws:3.4.1`). |
| **Permissão Negada (Spark Logs)** | Certifique-se de usar `-u 0` (root) no comando `docker exec` para que o Spark possa criar diretórios de cache temporários. |
| **Python: ModuleNotFoundError** | Rode `pip install -r requirements.txt` novamente. |
