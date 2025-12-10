# 2. Arquitetura do Projeto

## 2.1 Diagrama de Componentes

```mermaid
graph TD
    subgraph "External Source"
        LocalDisk[Local Dataset (datasets folder)]
    end

    subgraph "Ingestion Layer"
        Script[Python Ingest Script]
    end

    subgraph "Storage Layer (MinIO Data Lake)"
        Raw[(Raw Bucket\ncsv)]
        Bronze[(Bronze Bucket\nparquet)]
        Silver[(Silver Bucket\nparquet)]
    end

    subgraph "Processing Layer"
        SparkMaster[Spark Master]
        SparkWorker[Spark Worker]
    end

    subgraph "Analysis Layer"
        Jupyter[Jupyter Notebook]
    end

    LocalDisk -->|Read Files| Script
    Script -->|Upload .csv| Raw
    Raw -->|Read| SparkMaster
    SparkMaster -->|Processing| SparkWorker
    SparkWorker -->|Write .parquet| Bronze
    Bronze -->|Read/Transform| SparkMaster
    SparkMaster -->|Write Aggregations| Silver
    Silver -->|Read| Jupyter
```

## 2.2 Fluxo do Pipeline
1.  **Ingestão**: O script `src/ingest.py` lê os arquivos CSV (`movies.csv`, `ratings.csv`) diretório local `datasets/ml-latest-small` e faz o upload para o bucket `raw` no MinIO.
2.  **Processamento (Raw -> Bronze)**: O Spark lê os CSVs da camada `raw`, remove linhas nulas, infere schemas e salva em formato **Parquet** na camada `bronze`.
3.  **Processamento (Bronze -> Silver)**: O Spark lê a camada `bronze`, realiza joins entre tabelas (Ratings + Movies), calcula médias e contagens, e explode gêneros. O resultado é salvo na camada `silver` otimizado para leitura.
4.  **Análise**: O Jupyter Notebook consome os dados da camada `silver` via biblioteca `s3fs`/`pandas` para gerar gráficos.

## 2.3 Detalhes das Ferramentas

| Componente | Tecnologia | Versão | Função |
| :--- | :--- | :--- | :--- |
| **Container Engine** | Docker | Latest | Orquestração do ambiente. |
| **Storage** | MinIO | Latest | Object Storage compatível com S3 (Data Lake). |
| **Processing** | Apache Spark | 4.0.1 (Hadoop 3.4.1) | Motor de processamento distribuído. |
| **Language** | Python | 3.8+ | Scripts de automação e PySpark. |
| **Analysis** | Jupyter / Pandas | Latest | Ferramentas de Data Science interativo. |

## 2.4 Decisões Técnicas (Trade-offs)

### Armazenamento: MinIO vs HDFS
*   **Decisão**: Uso do MinIO.
*   **Por que**: Simula melhor ambientes de nuvem modernos (como AWS S3) do que HDFS, além de ser mais leve para rodar em containers locais e desacoplar computação de armazenamento.

### Processamento: Spark vs Pandas
*   **Decisão**: Uso do Apache Spark.
*   **Por que**: Embora Pandas fosse suficiente para o volume de dados do teste ("small"), o Spark foi escolhido para atender ao requisito de escalabilidade e demonstração de competência em Big Data. O código está pronto para escalar para Terabytes de dados sem refatoração.

### Formato de Arquivo: Parquet vs CSV
*   **Decisão**: Salvar camadas Bronze e Silver em Parquet.
*   **Por que**: Parquet é um formato colunar que oferece alta compressão e performance de leitura (IO) para cargas de trabalho analíticas, além de preservar o schema dos dados (tipagem).

## 2.5 Governança e Qualidade
*   **Separação em Camadas**: Garante que dados brutos nunca sejam perdidos (Raw) e que haja uma "single source of truth" refinada (Silver).
*   **Schema Enforcement**: O Spark define tipos de dados estritos durante a escrita em Parquet.
*   **Idempotência**: Os scripts de ingestão e processamento são projetados para serem executados múltiplas vezes sem duplicar dados incorretamente (modo `overwrite` no Spark).
