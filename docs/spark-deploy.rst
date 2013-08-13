Spark Master
============
- Create a spark master::
  
  $ onetemplate instantiate <template-id> --name cluster1.master

- Login to the master and generate a key pair::

  $ ssh-keygen -t rsa -C "master-VMNAME"

- Add the public key from ~/.ssh/id_rsa.pub to ~/.ssh/authorized_keys
- Note the IP address of the master.

Spark Slaves
============
-  On your local machine add the Master's public key to the slave template::
  
  $ onetemplate update <template-id>
  
  This will open the template in your text editor and you can paste the public
  key in USER_PUBKEY
- Run the deploy script::
  
  $ /path/to/script/spark_deploy.py -c <cluster_name> -n  <num_slaves> -m \
  <master_ip> 

- This should spawn ``<n>`` number of slaves and write the slaves hostnames to
  the master's spark directory.

- You can also specify the options in conf/defaults.py. Please note that the 
  command line options override the options set in defaults.py

- Login to the master and fire up everything::
  
  $ /path/to/spark/bin/start-all.sh

