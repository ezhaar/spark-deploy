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
spark_dir = "/home/admin/SPARK/spark/conf/"
on_username = "izhaar"
