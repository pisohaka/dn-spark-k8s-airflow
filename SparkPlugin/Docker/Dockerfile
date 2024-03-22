FROM apache/airflow:2.8.0-python3.11
WORKDIR /opt/airflow
COPY SparkPlugin/Docker/requirements.txt .
RUN pip install -r requirements.txt
USER root
RUN sudo apt-get update -y
RUN sudo apt-get install openjdk-17-jdk -y