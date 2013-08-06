#!/usr/bin/python


import subprocess
import argparse
import re


def donkey_work(cluster_name, num_slaves):

    create_master = "onetemplate instantiate 40 --name "
    create_slaves = "onetemplate instantiate 41 --name "

    master_conf = {}
    print("Creating Master Node with the command:\n" + create_master)

    print("Creating Slave Nodes...")
    try:
        for i in range(1, num_slaves + 1):
            # name the slave
            slave_name = "slave_" + str(i) + "." + cluster_name
            slave_output = subprocess.Popen(["onetemplate", "instantiate",
                                             "42", "--name", slave_name],
                                            stdout=subprocess.PIPE
                                            ).communicate()[0]

            slave_id = slave_output.strip('VM ID: ').strip('\n')
            # get master's public key
            # copy master's public key to slave's authorized_keys
            master_conf[slave_id] = "IP_ADD"
            vm_info = subprocess.Popen(["onevm", "show", str(slave_id)],
                                       stdout=subprocess.PIPE).communicate()[0]
            ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', vm_info)

        print(master_conf)
        status = 0
    except:
        status = 1
        raise

    print("Done...")
    return status


def main():

    parser = argparse.ArgumentParser(description="Create a Spark Cluster on "
                                     "PDC Cloud.")
    parser.add_argument("-c", "--name", metavar="", dest="cluster_name",
                        action="store", required=True, help="Name for the"
                        "cluster.")
    parser.add_argument("-n", "--num-slaves", metavar="", dest="num_slaves",
                        type=int, action="store", required=True,
                        help="Number of slave nodes to spawn.")
    parser.add_argument("-m", "--master-ip", metavar="", dest="master_ip",
                        action="store", required=True,
                        help = "Ip address of Master")

    args = parser.parse_args()
    cluster_name = args.cluster_name
    num_slaves = args.num_slaves
    master_ip = args.master_ip

    print("Cluster name will be set to: " + cluster_name)
    print("To avoid HOSTNAME conflicts, Please verify that cluster name is"
          "unique... Continue (y/n): ")
    status = donkey_work(cluster_name, num_slaves)
    if status == 0:
        print ("Done... Created the cluster")
    else:
        print("Error")

if __name__ == "__main__":
    main()
