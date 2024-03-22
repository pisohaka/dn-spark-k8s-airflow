from datetime import datetime
from airflow.decorators import dag, task
import requests

@dag(
    schedule=None,
    start_date= datetime(2024, 3, 1),
)
def spark_livy():

    @task()
    def submit():

        headers = {
        'Content-Type': 'application/json',
        }

        data = '''{
                "name": "test-001", 
                "className": "org.apache.spark.examples.SparkPi", 
                "numExecutors": 1,
                "file": "local:///opt/spark/examples/src/main/python/pi.py",
                "conf": { 
                    "spark.kubernetes.driver.pod.name" : "spark-pi-driver-001",
                    "spark.kubernetes.container.image" : "apache/spark-py",
                    "spark.kubernetes.namespace" : "airflow",
                    "spark.kubernetes.executor.request.cores": "0.1"
                        }
                    }'''

        response = requests.post('http://livy:8998/batches/', headers=headers, data=data)
        
        print(response.json())
        
        pass

    submit = submit()

spark_livy()