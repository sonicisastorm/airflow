from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count

# Start Spark session
spark = SparkSession.builder.appName("TaxiDataProcessing").getOrCreate()

# Read dataset
df = spark.read.parquet("/opt/airflow/dags/data/yellow_tripdata_2024-01.parquet")

# --- Narrow Dependencies ---
# 1. Filter trips with fare > 10
filtered_df = df.filter(col("fare_amount") > 10)

# 2. Add column trip duration in minutes
df_with_duration = filtered_df.withColumn(
    "trip_duration_min",
    (col("tpep_dropoff_datetime").cast("long") - col("tpep_pickup_datetime").cast("long"))/60
)

# --- Wide Dependencies ---
# 3. Group by payment type and get avg fare
agg_df = df_with_duration.groupBy("payment_type").agg(
    avg("fare_amount").alias("avg_fare"),
    count("*").alias("trip_count")
)

agg_df.show()

# Save results to output folder
agg_df.write.mode("overwrite").parquet("/opt/airflow/dags/output/taxi_results")

spark.stop()
