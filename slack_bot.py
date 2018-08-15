#!/usr/local/bin/python
import sys
import datetime
import os
import sys
import argparse
import subprocess 
from subprocess import Popen, PIPE
import hashlib
import pipes
import logging


def remove_file(dest):
       rm='rm -f ' + dest
       print "Erasing the file:",dest
       deli='touch ' + dest
       client.exec_command(deli)
       stdin_f,stdout_f,stderr_f = client.exec_command(rm)

def file(src,dest):
            file_exist='ls ' + dest
            stdin_f,stdout_f,stderr_f = client.exec_command(file_exist)
            if not stdout_f.readlines():
               file_check=False
            else:
               file_check=True

            chk_src='cksum ' + src                   
            p=subprocess.Popen(chk_src, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout.readlines():
              check_sum1=line.split(' ', 1)[0]
            retval = p.wait()

            checksum_dest='cksum ' + dest
            clause='touch ' + dest
            stdin1,stdout1,stderr1 = client.exec_command(clause)
            stdin1,stdout1,stderr1 = client.exec_command(checksum_dest)
            for line in stdout1.readlines():
              check_sum2=line.split(' ', 1)[0]

            if file_check==False:
               print "Transfering the file"
               sftp = client.open_sftp()
               sftp.put(src, dest)
               sftp.close()
            elif file_check==True and check_sum1!=check_sum2 :
               print "Transfering the file"
               sftp = client.open_sftp()
               sftp.put(src, dest)
               sftp.close()
            elif file_check==True and check_sum1==check_sum2: 
               logging.info("no changes, so skipping transfer")

            else:
               logging.info("Exception")
 
            if args.chmod :
              perm=str(args.chmod)
              mod='chmod ' + perm + ' ' + dest
              stdin1,stdout1,stderr1 = client.exec_command(mod)
              print stdout1.readlines()
            if args.chown :
              own='chown ' + args.chown + ' ' + dest 
              stdin1,stdout1,stderr1 = client.exec_command(own)
              print stdout1.readlines()

def service_action(package,do):
  to_do='service ' + package + ' ' + do
  stdin1,stdout1,stderr1 = client.exec_command(to_do)
  logging.info(stdout1.readlines())

def install_function(package):
     check_pack="dpkg -l | grep " + package + " | awk {'print $2'} | head -n 1 " #  > /tmp/file_local"
     print check_pack
     stdin1,stdout1,stderr1 = client.exec_command(check_pack)
     installed = None
     deb=str(stdout1.read())
     for line in stdout1:
           if package in line:
             installed = True   
     if installed!=True and args.install==True :
       print "Installing " + package
       ins_pack='sudo apt-get install '+ package + ' -y'
       stdin1,stdout1,stderr1 = client.exec_command(ins_pack)
       print stdout1.read()
     elif installed==True and args.remove==True :
       print "Removing " + package
       del_pack='sudo apt-get remove '+ package + ' -y'
       stdin1,stdout1,stderr1 = client.exec_command(del_pack)
       print stdout1.read()
     elif installed != True and args.remove == True :
       print "Package is not installed to remove"
     elif installed == True:
       print "Package is already installed or error attempting to install"
     else:
       print "Exception in installing"
       print "err:",stderr1.read()

if __name__ == '__main__':
            logging.basicConfig(level=logging.INFO)
            old_stdout = None
            now = datetime.datetime.now()
            helptitle = " list  of argument"
            parser = argparse.ArgumentParser(description=helptitle)
            parser.add_argument("-p", "--package", help="specify the package to download")
            parser.set_defaults(package=False)  
            parser.add_argument("-i", "--install", dest='install', action='store_true', help="set true for package installation")
            parser.set_defaults(install=False)
            parser.add_argument("-r", "--remove", dest='remove', action='store_true', help="set true for package removal")
            parser.set_defaults(remove=False) 
            parser.add_argument("-e", "--erase", dest='erase', action='store_true', help="set true for file removal")
            parser.set_defaults(erase=False)
            parser.add_argument("-d", "--do", help="set service action")
            parser.set_defaults(action=False)
            parser.add_argument("-f", "--file", help="set file")
            parser.set_defaults(file=False)
            parser.add_argument("-P", "--destfile", help="set Path")
            parser.set_defaults(destfile=False)
            parser.add_argument("-m", "--chmod", help ="change file permission")
            parser.set_defaults(chmod=False)
            parser.add_argument("-o", "--chown", help ="change file ownership")
            parser.set_defaults(chown=False)
            parser.add_argument("-b", "--host", type=str, help ="ip addr of remote host")
            parser.set_defaults(host=False)        
            parser.add_argument("-u", "--user", help ="username for the remote user")
            parser.set_defaults(user=False)
            parser.add_argument("-s", "--passwd", help ="passwd for the host")
            parser.set_defaults(passwd=False)
            args = parser.parse_args()

            if any( [not args.passwd, not args.host, not args.user]):
               print "Provide password,host,user"
               exit()

            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            host=args.host
            password =str(args.passwd)
            username=str(args.user)
            client.connect(host, username = username, password = password)

#bootstrap
#            sftp = client.open_sftp()
#            sftp.put('int/bootstrap.sh', '/root/bootstrap.sh')
#            sftp.close()
#            stdin,stdout,stderr = client.exec_command('(cd /root; bash bootstrap.sh)')
#            for line in stdout:
#                print line

            if args.package and args.install == True:
                      install_function(args.package)

            if all([args.package, args.do]):
                      service_action(args.package,args.do)

            if args.file and args.destfile:
                file(args.file,args.destfile)
                  
            if args.erase:
               remove_file(args.destfile)

            client.close()
