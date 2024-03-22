# Запуск Spark приложений в Kubernetes с помощью Airflow
Репозитории представляет из себя учебный материал для ознакомления с несколькими способами запуска Spark приложений.
Изучать материал стоит совместно со статьей или видео


## Работа с репозиторием
- [Предварительные работы](#Предварительные-работы)
- [Способы запуска](#Способы-запуска)

## Предварительные работы
Для работы необходим Airflow.
Запустить его можно с помощью Chart из данного репозитория:

```
helm upgrade --install -n airflow --create-namespace airflow \
  --set dags.gitSync.sshKey=<git_ssh_key> \
  --set data.metadataConnection.host=<pg_host> \
  --set data.metadataConnection.pass=<pg_pass> \
  --set data.metadataConnection.user=<pg_user> \
  --set data.metadataConnection.db=<pg_db> \
  --set images.airflow.repository=<airflow_image> \
  --set images.airflow.tag=latest .
```
В качестве образа необходимо использовать образ подходящий для способа запуска.

Теперь необходимо дать необходимые права сервисному аккаунту:
```
kubectl create clusterrolebinding spark-airflow-role --clusterrole=edit --serviceaccount=airflow:default --namespace=airflow
```
!Запуск спарк приложений будет происходить в namespace airflow и с помощью сервисного аккаунта airflow:default. В продовой среде лучше разделять namespaces и использовать отдельные сервисные аккаунты.

Также для демонстрации используется образ с ошибкой в Spark приложении:
```
docker build -t <your_registry>/spark-with-error -f SparkWithError/Dockerfile .
docker push <your_registry>/spark-with-error
```

## Способы запуска
### Spark Plugin
Для запуска необходимо испольовать соответствующий Airflow образ:
```
docker build -t <your_registry>/airflow-spark-plugin -f SparPlugin/Docker/Dockerfile .
docker push <your_registry>/airflow-spark-plugin
```
Пример DAG для запуска находится в AirflowDags/sparkPlugin.py 

### Spark Livy
Для запуска можно испольовать стандартный Airflow образ apache/airflow, т.к. способ не требует доп. пакетов.
Чтобы запустить Livy нужно собрать образ:
```
docker build -t <your_registry>/livy -f Livy/Docker/Dockerfile .
docker push <your_registry>/livy
```
После чего запустить k8s манифест, предварительно заменив в нем image Livy на свой:
```
export LIVY_IMAGE=<your_registry>/livy:latest
cat Livy/livy.yaml | envsubst | kubectl apply -f -
```
Пример DAG для запуска находится в AirflowDags/sparkLivy.py 

### Spark Plugin
Для запуска необходимо испольовать соответствующий Airflow образ:
```
docker build -t <your_registry>/airflow-spark-plugin -f SparPlugin/Docker/Dockerfile .
docker push <your_registry>/airflow-spark-plugin
```
После этого необходимо запустить [spark-operator](https://github.com/kubeflow/spark-operator/tree/master)
```
git clone git@github.com:kubeflow/spark-operator.git
helm upgrade --install -n airflow spark-operator spark-operator/charts/spark-operator-chart --set sparkJobNamespace=airflow
```
Далее необходимо добавить роль для запуска sparkapplications
```
kubectl apply -f SparkOperator/role.yaml
```
Пример DAG для запуска находится в AirflowDags/sparkOperator.py 