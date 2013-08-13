============
INTRODUCTION
============
Spark is a map-reduce cluster computing framework which is very similar to
Hadoop. However, unlike hadoop, spark provides in-memory data querying rather
than using disk I/O.

Spark is implemented in Scala and it provides API's in ``Scala``, ``python`` and
``java``. 

Scala is high level object oriented language which sits on top of JVM. 

Spark can run either on a single node in ``local`` mode or in cluster mode using
a resource manager such as ``Mesos, Yarn`` and ``Amazon EC2``. Spark can also be
run on a cluster without a resource manager in ``stand-alone`` mode.


INSTALLATION
------------

Requirements
------------

- Install Java::
  $ apt-get update && apt-get upgrade
  $ apt-get install default-jdk
  $ echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> ~/.bashrc

- Install Scala::
  
  $ wget http://www.scala-lang.org/downloads/distrib/files/scala-2.9.3.tgz
  
  $ tar -zxvf scala-2.9.3.tgz

  $ echo "export PATH=$PATH:/path/to/scala/bin" >> ~/.bashrc

- Install Spark::

  $ git clone git://github.com/mesos/spark.git
  
  $ cd spark
  
  $ sbt/sbt package
  
  $ mv conf/spark-env.sh-template conf/spark-env.sh
  Add the following line to your init file::
  ``export SCALA_HOME=/path/to/scala``

Test Run
--------

  $ ./run spark.examples.SparkPi local
  
Spark with HDFS
---------------

