FROM quay.io/jupyter/datascience-notebook
USER root

ARG openjdk_version="17"
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    "openjdk-${openjdk_version}-jre-headless" \
    ca-certificates-java \
    default-libmysqlclient-dev \
    build-essential  \
    pkg-config && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Kafka connector for Spark
RUN mkdir -p /opt/spark/jars && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.3/spark-sql-kafka-0-10_2.12-3.5.3.jar && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.1/kafka-clients-3.3.1.jar && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar && \
    wget -P /opt/spark/jars https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.3/spark-token-provider-kafka-0-10_2.12-3.5.3.jar

RUN pip install --upgrade pip 
COPY requirements.txt /home/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/requirements.txt && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" && \
    fix-permissions /opt/spark/jars

ENV PYTHONPATH="${PYTHONPATH}:/opt/spark/jars"
    
USER ${NB_UID}