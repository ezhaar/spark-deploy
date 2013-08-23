#!/bin/bash

# get masters ip
MASTER_IP=$1
MASTER_SSH="ssh -l admin -i $HOME/.ssh/id_rsa $MASTER_IP -o connectTimeout=5"
SSH_TEST=$($MASTER_SSH exit)
if [ $? == 0 ]; then
    echo "success"
else
    echo "ERROR: Could not connect to master"
    exit -1
fi

