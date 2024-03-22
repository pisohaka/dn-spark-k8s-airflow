from datetime import datetime

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 1),
    'depends_on_past': False,
}


with DAG(
    dag_id='spark_plugin',
    description='Запуск Spark приложения с помощью SparkSubmitOperator',
    catchup=False,
    schedule_interval=None,
    default_args=default_args,
    ) as dag:

    
    submit = SparkSubmitOperator(
        task_id='submit',
        conn_id='spark',
        application='local:///opt/spark/examples/src/main/python/pi.py',
        name='spark-pi',
        conf={
            'spark.kubernetes.namespace': 'airflow',
            'spark.submit.deployMode': 'cluster',
            'spark.kubernetes.container.image': 'apache/spark-py',
            'spark.kubernetes.container.image.pullPolicy': 'Always',
            'spark.executor.memory': '500m',
            'spark.executor.instances': '1',
            'spark.kubernetes.executor.request.cores': '0.1',
            'spark.driver.memory': '500m',
        }
    )

    submit
