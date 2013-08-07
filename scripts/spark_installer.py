#! /usr/bin/python
import os
from subprocess import Popen, PIPE


def ShellCommand(command):
    try:
        devnull = open(os.devnull, 'wb')
        sp = Popen(command, stdout=devnull, stderr=PIPE)
        devnull.close()
        return True
    except OSError as (errno, strerror):
        print (Binary Not Found: " + str(strerror))
        return False
    except Exception, error:
        print("Error while executing command: " + str(command))
        print(str(error))
        raise


def InstallJava():

    status = ShellCommand(["apt-get", "install", "default-jdk"])
    return status


def InstallHadoop():
    status = ShellCommand(["wget", "https://github.com/apache/hadoop-common/
                            "archive/release-1.1.2.tar.gz", "-P", "/tmp"])
    status = ShellCommand(["tar", "-xzf", "/tmp/release-1.1.2.tar.gz"])

def CheckPreReqs():
    status = {}
    java_installed = ShellCommand(["java", "-h"])
    if not java_installed:
        status['java'] = False
    else:
        status['java'] = True

    hadoop_installed = ShellCommand(["hadoop", "-h"])
    if not hadoop_installed:
        status['hadoop'] = False
    else:
        status['hadoop'] = True

    scala_installed = ShellCommand(["scala","-h"])
    if not scala_installed:
        status['scala'] = False
    else:
        status['scala'] = True

    return status


def main():

    status = CheckPreReqs()
    for key,val in status.items():
        print(key + " : " + str(val))
if __name__ == "__main__":
    main()

