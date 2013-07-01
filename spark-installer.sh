#!/bin/bash -x

apt-get update > /dev/null 
apt-get -y upgrade > /dev/null

# Check if java is installed
command -v javac>/dev/null 2>&1 || { echo >&2 "I require java but it's not installed. Installing java"; sudo apt-get install -y default-jdk;}

# Initialize directories

DOWNLOAD_DIR=~/Downloads
HADOOP_DIR=/usr/local/hadoop-1.1.2
SCALA_DIR=/usr/local/scala-2.9.3
SPARK_DIR=/usr/local/spark

# if Downloads folder does not exist, create it
if [ ! -d $DOWNLOAD_DIR ]; then
        mkdir $DOWNLOAD_DIR
fi

# if java_home is not set
if [[! -z "$JAVA_HOME" ]]; then
        echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> ~/.profile
fi

# download the src for hadoop, scala and spark
cd $DOWNLOAD_DIR
wget http://mirrors.sonic.net/apache/hadoop/common/hadoop-1.1.2/hadoop-1.1.2.tar.gz -P $DOWNLOAD_DIR
wget http://www.scala-lang.org/downloads/distrib/files/scala-2.9.3.tgz -P $DOWNLOAD_DIR
git clone git@github.com/mesos/spark.git

#Extract hadoop and Scala
tar -xzf hadoop-1.1.2.tar.gz
tar -zxf scala-2.9.3.tgz

# Move hadoop and scala to system wide directories
cp -R hadoop-1.1.2 $HADOOP_DIR
cp -R scala-2.9.3 $SCALA_DIR
chmod -R 777 $HADOOP_DIR
chmod -R 777 $SCALA_DIR

# Update .profile
#if hadoop prefix is not set, then set it and add to path
if [[! -z "$HADOOP_PREFIX" ]]; then
        echo "export HADOOP_PREFIX=$HADOOP_DIR" >> ~/.profile
        echo "export PATH=$PATH:$HADOOP_PREFIX/bin" >> ~/.profile
        source ~/.profile
fi

#create directory for hadoop to store files
mkdir -p /home/admin/hadoop

# download hadoop conf files from git
wget https://raw.github.com/ezhaar/spark-0.7.2/master/core-site.xml -P $HADOOP_DIR/conf
wget https://raw.github.com/ezhaar/spark-0.7.2/master/mapred-site.xml -P $HADOOP_DIR/conf
wget https://raw.github.com/ezhaar/spark-0.7.2/master/hdfs-site.xml -P $HADOOP_DIR/conf
#set JAVA_HOME in hadoop config file
echo "export JAVA_HOME=/usr/lib/jvm/default-java" >> /usr/local/hadoop-1.1.2/conf/hadoop-env.sh

# Format the name node
hadoop namenode -format

echo "***** HADOOP DONE! *****"
echo "***** Now buildind Scala *****"
echo "***** Creating soft links for scala in /usr/bin ***** "

ln -s $SCALA_DIR/bin/scala /usr/bin/scala
ln -s $SCALA_DIR/bin/scalac /usr/bin/scalac
ln -s $SCALA_DIR/bin/fsc /usr/bin/fsc
ln -s $SCALA_DIR/bin/sbaz /usr/bin/sbaz
ln -s $SCALA_DIR/bin/sbaz-setup /usr/bin/sbaz-setup
ln -s $SCALA_DIR/bin/scaladoc /usr/bin/scaladoc
ln -s $SCALA_DIR/bin/scalap /usr/bin/scalap


# Now build Spark
cp -R $DOWNLOAD_DIR/spark $SPARK_DIR

mv $SPARK_DIR/conf/spark-env.sh.template spark-env.sh
echo "export SCALA_HOME=$SCALA_DIR" >> spark-env.sh

#set hadoop version in spark build
sed -i 'S|1.0.4|1.1.2|' $SPARK_DIR/project/SparkBuild.scala
cd $SPARK_DIR
sbt/sbt package


