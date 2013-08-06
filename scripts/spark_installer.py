#!/usr/bin/python

from subprocess import Popen, PIPE


def shell_command(command):
    try:
        sp = Popen(command, stdout=PIPE, stderr=PIPE)
        return True
    except:
        return False


def install_java():
    try:

        sp = Popen(["apt-get", "install", "default-jdk"])

    except:
        raise

def main():

    java_installed = shell_command(["java", ])
    if !java_installed:
        print ("Missing: Java")
        install_java()
    else:
        print("Installed: Java")
    hadoop_installed = shell_command(["hadoop", "--version"])
    if !hadoop_installed:
        print("Missing: Hadoop")
        install_hadoop()
    else:
        print("Installed: Hadoop")

if __name__ == "__main__":
    main()
