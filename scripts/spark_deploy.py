#!/usr/bin/python


from subprocess import Popen, PIPE
import argparse
import re
import sys
import conf.defaults as defaults


def Ssh(vm_ip, verbose=False):
    try:
        st = Popen(["ssh", "-l", "admin", "-i", "~/.ssh/id_rsa", vm_ip],
                   stdout=PIPE,
                   stderr=PIPE)
    except OSError as (errno, strerr):
        print("Could not login...\n User verbose for detailed error msg")
        if verbose:
            print(str(errno) + "\n" + str(strerr))

    return st


def GetOrGeneratePubKey(master_ip):
    out = Popen(["./master_keys.sh", master_ip], stdout = PIPE,
                stderr = PIPE)
    return out.communicate()[0].strip("\n")


def UpdateMasterPubKey(master_ssh_key, on_username):

    master_ssh_key = "'Master_SSH_KEY=" + "\"" + master_ssh_key + "\"'"
    out = Popen(["./update_master_ssh_key.sh", master_ssh_key, on_username],
                stdout = PIPE,
                stderr = PIPE)

    return out.communicate()[0]


def Scp(vm_ip, filename, spark_dir, verbose=False):

    try:
        dest = "admin@" + vm_ip + ":" + spark_dir
        print ("copying to " + dest)
        st = Popen(["scp", filename, dest],
                   stdout=PIPE,
                   stderr=PIPE)
    except OSError as (errno, strerr):
        print("Could not login...\n Use verbose for detailed error msg")
        if verbose:
            print(str(errno) + "\n" + str(strerr))

    return st


def SpawnSlaves(cluster_name, slave_template, num_slaves):

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
                            stdout=PIPE).communicate()[0]
            ip_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', vm_info)

            slaves_list[slave_id] = ip_list[0]
        print(slaves_list)

    except:
        raise

    print("Slaves Spawned...")
    return slaves_list


def CheckArgs(args):
    try:
        args.num_slaves = int(args.num_slaves)
        args.cluster_name = str(args.cluster_name)
        args.master_ip = str(args.master_ip)

# check that there are any slaves to create
        if args.num_slaves < 1:
            print("There are no slaves to create...")
            sys.exit(0)

# double check that more than 10 slaves is not a typo
        if args.num_slaves > 10:
            input = raw_input("Are you sure you want to create "
                              + args.num_slaves
                              + " Slaves? (y/n)")
            if input != 'y':
                print("OK, Give it another try")
                sys.exit(0)

# Check that master has a public ip address
        if (args.master_ip).startswith("192"):
            print("I need a public IP address. Exit...")
            sys.exit(0)

        return args
    except:
        print("please recheck your arguments")
        raise


def main():

    parser = argparse.ArgumentParser(description="Create a Spark Cluster on "
                                     "PDC Cloud.", epilog ="Example Usage: "
                                     "./spark_deploy.py -c cluster1 -n 5 -m "
                                     "10.10.10.10")

    parser.add_argument("-c", "--name", metavar="", dest="cluster_name",
                        action="store",
                        default=defaults.cluster_name,
                        help="Name for the cluster.")
    parser.add_argument("-n", "--num-slaves", metavar="", dest="num_slaves",
                        default=defaults.num_slaves,
                        type=int, action="store",
                        help="Number of slave nodes to spawn.")
    parser.add_argument("-m", "--master-ip", metavar="", dest="master_ip",
                        action="store", default=defaults.master_ip,
                        help="Ip address of Master")
    parser.add_argument("-v", "--verbose", dest="verbose",
                        action="store_true", help="verbose output")
    parser.add_argument("-D", "--dryrun", dest="dryrun",
                        action="store_true", help="Dry run")

    args = parser.parse_args()

# Verify arguments
    args = CheckArgs(args)

# If args verified and there were no errors
# set variables
    cluster_name = args.cluster_name
    num_slaves = args.num_slaves
    master_ip = args.master_ip
    verbose = args.verbose
    dryrun = args.dryrun
    filename = defaults.filename
    slave_template = defaults.slave_template
    spark_dir = defaults.spark_dir
    on_username = defaults.on_username

    if dryrun:
        print("\n")
        print("Username: " + str(on_username))
        print("Cluster Name: " + str(cluster_name))
        print("Master IP: " + str(master_ip))
        print("Number of Slaves: " + str(num_slaves))
        print("Slave template: " + str(slave_template))
        print("Spark Dir on Master: " + str(spark_dir))
        print("\n")
        sys.exit(0)
# Get the Master's public key

    master_key = GetOrGeneratePubKey(master_ip)
    print("\n")
    print("******** Got the master's SSH key **********")
    update_status = UpdateMasterPubKey(master_key, on_username)
    print("******** Updated master's SSH for user: " + on_username +
          " **********")
    print("\n")
# Now create the requested number of slaves
# confirm cluster name
    print("Cluster name will be set to: " + args.cluster_name)
    input = raw_input("To avoid HOSTNAME conflicts, Please verify that "
                      "cluster name is unique... Continue (y/n): ")
    if input == 'n':
        print("Ok, Exit...")
        sys.exit(0)

    slaves_dict = SpawnSlaves(cluster_name, slave_template, num_slaves)
    slave_hostnames = []
    print("\n")
    for slave_id, hostname in slaves_dict.items():
        print(hostname + " Created...")
        slave_hostnames.append(str(hostname))
    print("\n")
# save slaves hostnames to file
    slave_file = open(filename, "w")
    for host in slave_hostnames:
        slave_file.write(host + "\n")

# move slaves file to master's spark conf directory
    Scp(master_ip, filename, spark_dir, verbose)

    print("\n")
    print("*********** All Slaves Created *************")
    print("*********** Slaves file Copied to Master *************")
    print("*********** Check that all slaves are RUNNING *************")
    print("*********** Login to Master and run start_all.sh *************")
    print("\n")
if __name__ == "__main__":
    main()
