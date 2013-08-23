#!/usr/bin/python


# IP address of master VM (string)
master_ip = ""
# number of slaves to create (integer)
num_slaves = 1
# unique name for the cluster (string)
cluster_name = ""
# templated id to use for the slaves (string)
slave_template = "41"
#temp file to hold slave hostnames (string)
filename = "/tmp/slaves"
# remote username on master e.g. admin or root
remote_username = "admin"
#conf files directory for spark
spark_dir = "/home/"+remote_username+"/SPARK/spark/conf/"
