FROM ubuntu:xenial AS base

RUN apt-get update -qq > /dev/null && apt-get install -qq --yes --no-install-recommends \
    locales && \
    locale-gen en_US.UTF-8
ENV LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8"

RUN apt-get install -qq \
    apt-transport-https \
    curl \
    git \
    libkrb5-dev \
    maven \
    openjdk-8-jdk \
    python-dev \
    python-pip \
    python3-pip \
    software-properties-common \
    vim \
    wget \
    telnet \
    lsof


RUN add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/' && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    apt-get update && \
    apt-get -qq install r-base


RUN python -m pip install -U "pip < 21.0" && \
	apt-get remove -y python-setuptools && \
	python -m pip install "setuptools < 36" && \
	python -m pip install \
        cloudpickle \
        codecov \
        flake8 \
        flaky \
        "future>=0.15.2" \
        "futures>=3.0.5" \
        pytest \
        pytest-runner \
        requests-kerberos \
        "requests >= 2.10.0" \
        "responses >= 0.5.1"

RUN python3 -m pip install -U pip

WORKDIR /workspace

FROM base AS base-spark

ARG SPARK_ARC=spark-3.5.1-bin-hadoop3
ARG HADOOP_VERSION=3.3.1
ARG SPARK_VERSION=3.2.3
ARG ROOT_PATH=/opt

RUN mkdir -p ${ROOT_PATH}


ENV SPARK_HOME=${ROOT_PATH}/spark
ENV PATH=${PATH}:${SPARK_HOME}/bin
ENV SPARK_PACKAGE=${SPARK_ARC}

ADD https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz ${SPARK_PACKAGE}.tgz

RUN tar -xvzf ${SPARK_PACKAGE}.tgz -C ${ROOT_PATH}/ \
    && ln -s ${ROOT_PATH}/${SPARK_PACKAGE} ${SPARK_HOME} \
    && chown -R root:root ${SPARK_HOME} \
    && rm ${SPARK_PACKAGE}.tgz

WORKDIR ${SPARK_HOME}

FROM base-spark

ARG LIVY_VERSION=0.8.0-incubating_2.12
ARG ROOT_PATH=/opt

RUN apt-get update \
    && apt-get install -y unzip

ENV LIVY_HOME=${ROOT_PATH}/livy
ENV LIVY_PACKAGE=apache-livy-${LIVY_VERSION}-bin

ADD https://dlcdn.apache.org/incubator/livy/0.8.0-incubating/apache-livy-0.8.0-incubating_2.12-bin.zip ${LIVY_PACKAGE}.zip

RUN unzip ${LIVY_PACKAGE}.zip 1>/dev/null \
  && mv ${LIVY_PACKAGE} ${ROOT_PATH}/ \
  && ln -s ${ROOT_PATH}/${LIVY_PACKAGE} ${LIVY_HOME} \
  && chown -R root:root ${LIVY_HOME} \
  && rm ${LIVY_PACKAGE}.zip

WORKDIR ${LIVY_HOME}

