from airflow import DAG
from airflow.operators.bash import BashOperator
from pendulum import datetime

with DAG(
    dag_id="spark_taxi_job",
    start_date=datetime(2025, 6, 1),
    schedule="*/10 * * * *",   # every 10 minutes
    catchup=False,
    tags=["spark", "taxi"],
) as dag:

    spark_submit_task = BashOperator(
        task_id="spark_submit_taxi",
        bash_command="""
spark-submit \
  --master local[*] \
  --conf spark.eventLog.enabled=false \
  /opt/airflow/dags/process_taxi_data.py
"""
    )
