# task

This is a Configuration Management Tool for Ubuntu:
* Tool can modify file's metadata (owner, group, mode)
* Tool allows installing and removing Debian packages 
* Tool provide some mechanism for restarting a service
* Preserve idempotency for file transfer but not for package installation and removal[Need to be fixed]
* Tool also need to fully utilize logging module instaed of print

Download and copy the script to your PATH to call it as slack_bot:
  ln -s slack_bot.py /usr/bin/local/slack_bot  
  echo $PATH=$PATH:/usr/bin/local/

This tool uses argpraser and require input to be passed to them. Options available:
slack_bot -h
usage: slack_bot.py [-h] [-p PACKAGE] [-i] [-r] [-e] [-d DO] [-f FILE]
                    [-P DESTFILE] [-m CHMOD] [-o CHOWN] [-b HOST] [-u USER]
                    [-s PASSWD]

list of argument

optional arguments:
  -h, --help            show this help message and exit
  -p PACKAGE, --package PACKAGE
                        specify the package to download
  -i, --install         set true for package installation
  -r, --remove          set true for package removal
  -e, --erase           set true for file removal
  -d DO, --do DO        set service action
  -f FILE, --file FILE  set file
  -P DESTFILE, --destfile DESTFILE
                        set Path
  -m CHMOD, --chmod CHMOD
                        change file permission
  -o CHOWN, --chown CHOWN
                        change file ownership
  -b HOST, --host HOST  ip addr of remote host
  -u USER, --user USER  username for the remote user
  -s PASSWD, --passwd PASSWD
                        passwd for the host


I'll illustrate how to bring a simple hello world php on a web server:
To install the necessary package:
  *slack_bot -p "apache2 php5 " -i -b "1**.206.1.***" -u "***" -s "***"
  *slack_bot -p "libapache2-mod-php5" -i -b "1**.206.1.***" --u "***" -s "***"

To erase a file:
 *slack_bot -e -f "/var/www/html/*" -b "1**.206.1.***" -u "***" -s "***"
 Erasing the file: /var/www/html/*

To Copy the index file:
 *slack_bot -f "int/index.php" -P "/var/www/html/index.php" -b "1**.206.1.***" -u "***" -s "***"
 Transfering the file

To Bounce an appliaction:
 *slack_bot -p "apache2" -d "restart" -b "1**.206.1.***" -u "***" -s "***"
 [u' * Restarting web server apache2\n', u'   ...done.\n']
