from datetime import datetime
from airflow.decorators import dag, task
import requests

@dag(
    schedule=None,
    start_date= datetime(2024, 3, 1),
)
def spark_livy_error():

    @task()
    def submit():

        headers = {
        'Content-Type': 'application/json',
        }

        data = '''{
                "name": "test-002", 
                "className": "org.apache.spark.examples.SparkPi", 
                "numExecutors": 1,
                "file": "local:///opt/spark/examples/src/main/python/error_app.py",
                "conf": { 
                    "spark.kubernetes.driver.pod.name" : "spark-pi-driver-002",
                    "spark.kubernetes.container.image" : "spark-with-error",
                    "spark.kubernetes.namespace" : "airflow",
                    "spark.kubernetes.executor.request.cores": "0.1"
                        }
                    }'''

        response = requests.post('http://livy:8998/batches/', headers=headers, data=data)
        
        print(response.json())
        
        pass

    submit = submit()

spark_livy_error()