FROM apache/airflow:2.8.0-python3.11
WORKDIR /opt/airflow
COPY SparkOperator/Docker/requirements.txt .
RUN pip install -r requirements.txt