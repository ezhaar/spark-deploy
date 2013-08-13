#!/usr/bin/python


from subprocess import Popen, PIPE
import argparse
import re
import sys


def ssh(vm_ip, verbose=False):
    try:
        st = Popen(["ssh", "-l", "admin", "-i", "~/.ssh/id_rsa", vm_ip],
                   stdout=PIPE,
                   stderr=PIPE)
    except OSError as (errno, strerr):
        print("Could not login...\n User verbose for detailed error msg")
        if verbose:
            print(str(errno) + "\n" + str(strerr))

    return st


def scp(vm_ip, file, verbose=False):

    try:
        admin_login = "admin@" + vm_ip
        st = Popen(["scp", "-i", file, admin_login],
                   stdout=PIPE,
                   stderr=PIPE)
    except OSError as (errno, strerr):
        print("Could not login...\n User verbose for detailed error msg")
        if verbose:
            print(str(errno) + "\n" + str(strerr))

    return st


def spawn_slaves(cluster_name, slave_template, num_slaves):

    slaves_list = {}

    print("Creating Slave Nodes...")
    try:
        for i in range(1, num_slaves + 1):
            # name the slave
            slave_name = "slave" + str(i) + "." + cluster_name
            result = Popen(["onetemplate", "instantiate",
                            slave_template, "--name", slave_name],
                           stdout=PIPE).communicate()[0]

            slave_id = result.strip('VM ID: ').strip('\n')
            vm_info = Popen(["onevm", "show", str(slave_id)],
                            stdout=subprocess.PIPE).communicate()[0]
            ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', vm_info)

            slaves_list[slave_id] = ip_list[0]
        print(slaves_list)

    except:
        raise

    print("Done...")
    return slaves_list


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
                        help="Ip address of Master")
    parser.add_argument("-v", "--verbose", metavar="", dest="verbose",
                        action="store", default=False, help="verbose output")

    args = parser.parse_args()
    cluster_name = args.cluster_name
    num_slaves = args.num_slaves
    master_ip = args.master_ip
    verbose = args.verbose
    if num_slaves > 10:
        input = raw_input("Are you sure you want to create " + num_slaves +
                          " Slaves? (Y/n)")
        if input != 'Y':
            print("OK, Give it another try")
            sys.exit(0)

    print("Cluster name will be set to: " + cluster_name)
    input = raw_input("To avoid HOSTNAME conflicts, Please verify that cluster"
                      "name is unique... Continue (y/n): ")
    if input == 'n':
        print("you did not choose 'y' to Continue")
        print("system will exit now")
        sys.exit(0)

#    slaves_dict = spawn_slaves(cluster_name, num_slaves)
    slaves_dict={"192.168.1.150":"192.168.1.150"}
    slave_hostnames = []
    for slave_id, hostname in slaves_dict.items():
        print(hostname)
        slave_hostnames.insert(str(hostname))
    slave_file = open("/tmp/slaves", "w")
    slave_file.write(slave_hostnames)
    scp(master_ip, slave_file)


if __name__ == "__main__":
    main()
