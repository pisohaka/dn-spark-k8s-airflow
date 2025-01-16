from datetime import datetime
from airflow.decorators import dag

from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import (
    SparkKubernetesSensor,
)


@dag(
    schedule=None,
    start_date= datetime(2024, 3, 1),
)
def spark_operator_error():


    submit = SparkKubernetesOperator(
        task_id="submit",
        namespace="airflow",
        application_file="spark-application.yaml",
        do_xcom_push=False,
        params={"app_name": "spark-pi"},
        kubernetes_conn_id="kubernetes_default",
        log_events_on_failure=True,
        delete_on_termination=True,
        on_finish_action="delete_pod",
    )
    submit



spark_operator_error()
