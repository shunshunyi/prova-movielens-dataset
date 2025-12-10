# 1. Visão Geral do Trabalho

## 1.1 Descrição do Problema
O volume crescente de dados gerados por usuários em plataformas de streaming exige arquiteturas robustas para processamento e análise. Este projeto aborda o desafio de ingerir, limpar, transformar e analisar dados de avaliações de filmes (dataset MovieLens) para extrair insights sobre popularidade e preferências por gênero.

## 1.2 Objetivos do Sistema
O objetivo principal é construir um **Data Lake** funcional e um pipeline de dados **ETL (Extract, Transform, Load)** capaz de:
*   Ingerir dados brutos de fontes externas.
*   Armazenar dados de forma segura, escalável e organizada (camadas Raw, Bronze, Silver).
*   Processar grandes volumes de dados utilizando computação distribuída (Spark).
*   Disponibilizar dados tratados para análise de negócios e visualização.

### Justificativa Técnica
A escolha de uma arquitetura baseada em **Containers** (Docker), **Object Storage** (MinIO) e **Processing Engine** (Spark) simula um ambiente de Big Data moderno, permitindo escalabilidade horizontal e desacoplamento entre armazenamento e processamento.

## 1.3 Escopo da Solução

### Incluído
*   **Ingestão de Dados Locais**: Script automatizado para upload do dataset local para o Data Lake.
*   **Armazenamento**: Configuração de Data Lake com MinIO (S3 Compatible).
*   **Processamento Batch**: Job PySpark para limpeza, tipagem e agregações.
*   **Camadas de Dados**:
    *   **Raw**: CSV originais.
    *   **Bronze**: Dados convertidos para Parquet (limpeza leve).
    *   **Silver**: Dados agregados e enriquecidos (KPIs).
*   **Análise Exploratória**: Jupyter Notebook consumindo a camada Silver.
*   **Infraestrutura as Code**: Docker Compose.

### Não Incluído
*   Processamento em Streaming (Real-time).
*   Dashboards interativos (PowerBI/Tableau) - Foco em Notebook.
*   Deployment em Nuvem Pública (AWS/Azure/GCP) - Foco em ambiente local simulado.
*   API Rest para servir os dados (embora a arquitetura permita fácil acoplamento).

## 1.4 Pontos de Falha e Limitações

### Pontos de Falha (SPOF)
*   **MinIO**: Se o container do MinIO cair, todo o pipeline de escrita e leitura falha. Em produção, seria necessário um cluster MinIO ou serviço gerenciado S3.
*   **Spark Master**: Se o nó Master falhar, novos jobs não poderão ser agendados.
*   **Ingestão Manual**: O script de ingestão é disparado manualmente. Falha humana em não executar o script resulta em dados desatualizados.

### Limitações
*   **Latência**: O processamento é em batch (D-1 ou sob demanda), não sendo adequado para análises em tempo real (streaming).
*   **Volume de Dados**: A infraestrutura local (Docker Compose) é limitada pelos recursos da máquina host (RAM/CPU). Para Big Data real (Terabytes), seria necessário um cluster distribuído (AWS EMR / Databricks).

## 1.5 Trabalho Individual

Este projeto foi executado individualmente por **David Gilmour Souza**, que foi responsável por todas as etapas do desenvolvimento:

*   **Arquitetura**: Definição e implementação do Data Lake (MinIO) e containers Docker.
*   **Engenharia de Dados**: Desenvolvimento dos scripts de ingestão (Python) e pipeline de processamento (Spark).
*   **Análise de Dados**: Criação dos notebooks Jupyter e visualizações.
*   **Documentação**: Elaboração de todos os guias técnicos e documentação do projeto.
