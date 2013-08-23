#!/bin/bash

master_ssh_key=$1
on_username=$(oneuser list -l NAME | tail -1)

# remove already exisitng key
export EDITOR="sed -ie '/MASTER_SSH_KEY/d'"
oneuser update $on_username

#insert new key
export EDITOR="echo $master_ssh_key >> "
st=$(oneuser update $on_username)
if [ $? == 0 ]; then
    echo "$on_username Updated"
else
    echo "ERROR: could not update master key for $on_username"
fi
