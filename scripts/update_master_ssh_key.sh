#!/bin/bash

master_ssh_key=$1
on_username=$2

# remove already exisitng key
export EDITOR="sed -ie '/MASTER_SSH_KEY/d'"
oneuser update $on_username

#insert new key
export EDITOR="echo $master_ssh_key >> "
oneuser update $on_username
