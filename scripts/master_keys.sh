#!/bin/bash

# get masters ip
MASTER_IP=$1
username=$2
MASTER_SSH="ssh -l $username -i $HOME/.ssh/id_rsa $MASTER_IP -o connectTimeout=5"
# ssh to master
PUB_KEY=$($MASTER_SSH "cat ~/.ssh/id_rsa.pub")

# if key found
if [ $? == 0 ]; then
    echo $PUB_KEY

# if key not found, generate and add to authorized_keys
else 
    $($MASTER_SSH "ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -C $MASTER_IP")
    PUB_KEY=$($MASTER_SSH "cat ~/.ssh/id_rsa.pub")
    $($MASTER_SSH "cat ~/.ssh/id_rsa.pub>>~/.ssh/authorized_keys")

    echo $PUB_KEY

fi

