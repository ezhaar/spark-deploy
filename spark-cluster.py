#!/bin/python

import subprocess
import os
import argparse


parser = argparse.ArgumentParser(description='Create a Spark Cluster on PDC Cloud.')
parser.add_argument("-c","--name", metavar="", dest="cluster_name",
		action="store", required=True, help="Name for the cluster.")
parser.add_argument("-n","--num-slaves", metavar="", dest="num_slaves", type=int,
		action="store", required=True, help="Number of slave nodes to spawn.")
args = parser.parse_args()
cluster_name = args.cluster_name
num_slaves = args.num_slaves

print("To avoid HOSTNAME conflicts, Please verify that cluster name is unique.. Continue (y/n): ")
print("Creating Master Node...")
print("Creating Slave Nodes...")
print("Done...")
