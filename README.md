# Projeto de Ciência de Dados: Análise de Avaliações de Filmes

Bem-vindo à solução do desafio de Big Data / Ciência de Dados. Este repositório contém a implementação completa de um Data Lake e pipeline de processamento para dados do MovieLens.

## Documentação Oficial

Para atender aos requisitos de avaliação, a documentação está organizada detalhadamente na pasta `/docs`:

1.  **[Visão Geral](docs/1_overview.md)**
    *   Descrição do problema, objetivos, escopo e equipe.
2.  **[Arquitetura](docs/2_architecture.md)**
    *   Diagramas, fluxo de dados, stack tecnológico e decisões técnicas.
3.  **[Dicionário de Dados](docs/3_data_dictionary.md)**
    *   Origem dos dados e schemas das camadas Raw, Bronze e Silver.
4.  **[Guia de Execução](docs/4_user_guide.md)**
    *   Passo-a-passo detalhado para rodar o projeto do zero ("Read the Docs" style).

## Guia Rápido ("TL;DR")

Se você já conhece o projeto e quer apenas subir o ambiente:

```bash
# 1. Subir Infra
docker-compose -f infra/docker-compose.yml up -d

# 2. Ingerir Dados
pip install -r requirements.txt
python src/ingest.py

# 3. Processar (Via Docker)
docker exec -u 0 spark-master /opt/spark/bin/spark-submit \
  --packages org.apache.hadoop:hadoop-aws:3.4.1 \
  --master spark://spark-master:7077 \
  /opt/spark/process.py

# 4. Analisar
jupyter notebook notebooks/analysis.ipynb
```

## Estrutura do Repositório

```
/
├── docs/           # Documentação completa (Visão geral, Arq, Dados, Manual)
├── infra/          # Configuração Docker e serviços (Spark, MinIO)
├── notebooks/      # Análises e Visualizações (Jupyter)
├── src/            # Código fonte (Ingestão e Processamento Spark)
├── datasets/       # Dados do MovieLens (ml-latest-small)
├── requirements.txt # Dependências Python
└── README.md       # Este índice
```

---
*Projeto desenvolvido para a Prova Prática de Ciência de Dados e Big Data.*
