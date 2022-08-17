# ESTCP-volttorn-EMS-agents
new line 
INSTALLING VOLTTRON SOURCE
1.	Run sudo apt-get update
2.	Run sudo apt-get install build-essential python-dev openssl libssl-dev libevent-dev git
3.	Run git clone https://github.com/VOLTTRON/volttron
4.	Run cd <volttron clone directory>
5.	Run python bootstrap.py
6.	Run source env/bin/activate
7.	Run volttron -vv -l volttron.log&

PYTHON 3 TO VOLTTRON DB_CONNECTOR
1.	Place watchdog.py in <volttron clone directory>/scripts/
2.	In A Separate Shell Window (ssh into box in different tab) Run nohup python3 <volttron clone dir>/watchdog.py <volttron clone directory>/scripts/db_outfile.txt

VOLTTRON EMS INSTALL
1.	Replace <volttron install dir>/examples/ListenerAgent with supplied ListenerAgent directory 
2.	Change "file" value in supplied filewatchpublisher.config to /path/to/db_outfile.txt
3.	Replace <volttron install dir>/services/ops/FileWatchPublisher/filewatchpublisher.config with prepared filewatchpublisher.config
4.	Run python <volttron install dir>/scripts/install-agent.py -s <volttron install dir>/examples/ListenerAgent/ -c examples/ListenerAgent/config
5.	Run python <volttron install dir>/scripts/install-agent.py -s <volttron install dir>/services/ops/FileWatchPublisher/ -c services/ops/FileWatchPublisher/filewatchpublisher.config
6.	Run volttron-ctl start --name listeneragent-3.2
7.	Run volttron-ctl start --name filewatchpublisheragent-0.1
8.	Copy custom_agents directory to <volttron clone dir>
9.	Run python <volttron clone dir>/scripts/install-agent.py -s <volttron clone dir>/custom_agents/DBAgent
10.	Run volttron-ctl config store dbagentagent-0.1_1 config <volttron clone dir>/custom_agents/DBAgent/config
11.	Run volttron-ctl start --name dbagentagent-0.1
12.	Place batch_install.py in <volttron clone dir>/scripts/
13.	Run mkdir <volttron clone dir>/scripts/configs
14.	Create a file called ipfile.txt with the ip address of each DER to be installed on it's own line. Follow ips.txt format
15.	Place ipfile.txt in <volttron clone dir>/scripts/
16.	Run python batch_install.py <volttron clone dir>/scripts/ipfile.txt <volttron clone dir>/scripts/configs/ 0

Directory Structure Sample on Next Page

Before running batch_install.py your directory structure should look something like this:

volttron
    | custom_agents
    |----| DBAgent
    |----| StateChangeAgent
    | scripts
    |----| configs
    |----| batch_install.py
    |----| Other VOLTTON Scripts
    | Other VOLTTRON dirs
