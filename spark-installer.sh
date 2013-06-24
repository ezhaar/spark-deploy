#!/bin/bash

apt-get update && apt-get -y upgrade > /dev/null

command -v javac>/dev/null 2>&1 || { echo >&2 "I require java but it's not installed. Installing java"; sudo apt-get install -y default-jdk;}

DOWNLOAD_DIR=~/Downloads
HADOOP_DIR=/usr/local/hadoop-1.1.2
SCALA_DIR=/usr/local/scala-2.9.3

if [ ! -d $DOWNLOAD_DIR ]; then
        mkdir $DOWNLOAD_DIR
fi

if [[! -z "$JAVA_HOME" ]]; then
        echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> ~/.profile
fi

# download the src for hadoop, scala and spark

wget http://mirrors.sonic.net/apache/hadoop/common/hadoop-1.1.2/hadoop-1.1.2.tar.gz -P $DOWNLOAD_DIR
wget http://www.scala-lang.org/downloads/distrib/files/scala-2.9.3.tgz -P $DOWNLOAD_DIR

cd $DOWNLOAD_DIR
tar -xzf hadoop-1.1.2.tar.gz
tar -zxf scala-2.9.3.tgz

cp -R hadoop-1.1.2 $HADOOP_DIR
cp -R scala-2.9.3 $SCALA_DIR
chmod -R 777 $HADOOP_DIR
chmod -R 777 $SCALA_DIR

# Update .profile

if [[! -z "$HADOOP_PREFIX" ]]; then
        echo "export HADOOP_PREFIX=$HADOOP_DIR" >> ~/.profile
        echo "export PATH=$PATH:$HADOOP_PREFIX/bin" >> ~/.profile
        source ~/.profile
fi

#create directory for hadoop to store files
mkdir -p /home/admin/hadoop

# download conf files from git
wget https://raw.github.com/ezhaar/spark-0.7.2/master/core-site.xml -P $HADOOP_DIR/conf
wget https://raw.github.com/ezhaar/spark-0.7.2/master/mapred-site.xml -P $HADOOP_DIR/conf
wget https://raw.github.com/ezhaar/spark-0.7.2/master/hdfs-site.xml -P $HADOOP_DIR/conf

echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /usr/local/hadoop-1.1.2/conf/hadoop-env.sh

# Format the name node
hadoop namenode -format

echo "***** Creating soft links for scala in /usr/bin ***** "

ln -s $SCALA_DIR/bin/scala /usr/bin/scala
ln -s $SCALA_DIR/bin/scalac /usr/bin/scalac
ln -s $SCALA_DIR/bin/fsc /usr/bin/fsc
ln -s $SCALA_DIR/bin/sbaz /usr/bin/sbaz
ln -s $SCALA_DIR/bin/sbaz-setup /usr/bin/sbaz-setup
ln -s $SCALA_DIR/bin/scaladoc /usr/bin/scaladoc
ln -s $SCALA_DIR/bin/scalap /usr/bin/scalap
