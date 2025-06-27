from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os
import psycopg2

# Add path to import our ingest function
sys.path.append('/opt/airflow/app')
from my_ingest import process_hts

# Function to run our data ingest
def run_ingestion():
    conn = psycopg2.connect(
        host="db",
        port=5432,
        dbname="htsdb",
        user="htsuser",
        password="htspass"
    )
    process_hts("https://www.usitc.gov/sites/default/files/tata/hts/hts_2025_revision_15_json.json", conn)
    conn.close()

# DAG settings
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

# Define the DAG
with DAG(
    'hts_ingest_dag',
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule_interval='*/10 * * * *',
    catchup=False
) as dag:

    ingest_task = PythonOperator(
        task_id='run_hts_ingestion',
        python_callable=run_ingestion
    )
