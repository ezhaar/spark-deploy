#!/bin/bash

# get masters ip
MASTER_IP=$1
MASTER_SSH="ssh -l admin -i $HOME/.ssh/id_rsa $MASTER_IP "
# ssh to master
PUB_KEY=$($MASTER_SSH "cat ~/.ssh/id_rsa.pub")
if [ $? == 0 ]; then
    echo $PUB_KEY
else 
    echo "public key not found"
    $($MASTER_SSH "ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -C $MASTER_IP")
    
fi

# check if id_rsa.pub exists

# if yes then copy

# if no then generate and copy


