from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, count, desc, explode, split, col

def main():
    spark = SparkSession.builder \
        .appName("MovieLensProcessing") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .getOrCreate()
    
    # --- Ingestion / Bronze Layer ---
    print("Reading from Raw layer...")
    # NOTE: In a real cluster mapped via docker-compose, 'minio' hostname works. 
    # From outside, we use localhost. This script runs INSIDE spark container usually.
    
    ratings_df = spark.read.option("header", "true").option("inferSchema", "true").csv("s3a://raw/ratings.csv")
    movies_df = spark.read.option("header", "true").option("inferSchema", "true").csv("s3a://raw/movies.csv")

    # Clean / Join
    print("Processing to Bronze layer...")
    # Basic cleaning: drop nulls
    ratings_clean = ratings_df.dropna()
    movies_clean = movies_df.dropna()
    
    # Save Bronze (Just purely clean data, converted to parquet)
    ratings_clean.write.mode("overwrite").parquet("s3a://bronze/ratings")
    movies_clean.write.mode("overwrite").parquet("s3a://bronze/movies")

    # --- Processing / Silver Layer ---
    print("Processing to Silver layer...")
    
    # Join
    joined_df = ratings_clean.join(movies_clean, "movieId")
    
    # Aggregation 1: Average rating per movie
    movie_ratings = joined_df.groupBy("movieId", "title") \
        .agg(avg("rating").alias("avg_rating"), count("rating").alias("count")) \
        .filter(col("count") > 10) \
        .orderBy(desc("avg_rating"))
        
    # Aggregation 2: Movies per genre (need to explode genres)
    # genres format is "Adventure|Animation|Children|Comedy|Fantasy"
    genres_df = movies_clean.withColumn("genre", explode(split(col("genres"), "\\|")))
    genre_counts = genres_df.groupBy("genre").count().orderBy(desc("count"))
    
    # Save Silver
    movie_ratings.write.mode("overwrite").parquet("s3a://silver/movie_ratings")
    genre_counts.write.mode("overwrite").parquet("s3a://silver/genre_counts")
    
    print("Processing complete.")
    spark.stop()

if __name__ == "__main__":
    main()
