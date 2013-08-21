Spark Master
============
- Create a spark master::
  
  $ onetemplate instantiate <template-id> --name cluster1.master

- Note the IP address of the master.
- Make sure that your templates (master and slave) source .bashrc at login

Spark Slaves
============

- Run the deploy script::
  
  ``$ /path/to/script/spark_deploy.py -c <cluster_name> -n  <num_slaves> -m \
  <master_ip>`` 

- This will spawn ``<n>`` number of slaves and write the slaves hostnames to
  the master's spark directory.

- You can also specify the options in conf/defaults.py. Please note that the 
  command line options override the options set in defaults.py

- Login to the master and fire up everything::
  
  $ /path/to/spark/bin/start-all.sh

