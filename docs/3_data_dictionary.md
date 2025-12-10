# 3. Dicionário de Dados

## 3.1 Origem dos Dados
*   **Dataset**: MovieLens Latest Small
*   **Fonte**: GroupLens Research (Universidade de Minnesota)
*   **URL**: [https://files.grouplens.org/datasets/movielens/ml-latest-small.zip](https://files.grouplens.org/datasets/movielens/ml-latest-small.zip)

## 3.2 Camada Raw (Dados Brutos)
Arquivos CSV ingeridos sem alteração.

### `ratings.csv`
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `userId` | Integer | ID único do usuário que fez a avaliação. |
| `movieId` | Integer | ID único do filme (chave estrangeira). |
| `rating` | Float | Nota dada ao filme (0.5 a 5.0). |
| `timestamp` | Long | Data/hora da avaliação (epoch). |

### `movies.csv`
| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `movieId` | Integer | ID único do filme. |
| `title` | String | Título do filme (inclui ano). |
| `genres` | String | Lista de gêneros separados por pipe `|` (ex: "Adventure\|Children"). |

## 3.3 Camada Silver (Dados Processados)
Dados limpos, enriquecidos e agregados para análise.

### `movie_ratings`
Tabela agregada com métricas por filme.
*   **Localização**: `s3a://silver/movie_ratings`
*   **Formato**: Parquet

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `movieId` | Integer | ID do filme. |
| `title` | String | Título do filme. |
| `avg_rating` | Double | Média aritmética das notas recebidas. |
| `count` | Long | Número total de avaliações recebidas. |

*Filtro aplicado*: Apenas filmes com mais de 10 avaliações.

### `genre_counts`
Tabela de distribuição de popularidade por gênero.
*   **Localização**: `s3a://silver/genre_counts`
*   **Formato**: Parquet

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `genre` | String | Nome do gênero (após explosão da coluna `genres`). |
| `count` | Long | Quantidade total de filmes associados a esse gênero no dataset. |
