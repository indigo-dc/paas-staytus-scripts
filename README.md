# paas-staytus-scripts
Collection of python scripts for monitoring PaaS services with [staytus](https://staytus.co/)

## Deployment

Clone this repository and install the scripts:

````
git clone https://github.com/indigo-dc/paas-staytus-scripts.git
cd paas-staytus-scripts
pip3 install .
````

The executable script `paas-staytus-health` will be installed in the user bin path, e.g.:

````
$ which paas-staytus-health
/usr/local/bin/paas-staytus-health
````

The script needs to be configured in order to run:
````
$ paas-staytus-health
usage: paas-staytus-health [-h] --conf-file CONF_FILE
paas-staytus-health: error: the following arguments are required: --conf-file
````

As starting point, you can use the configuration file `config.ini` installed with the package, completing the empty fields (all of them are mandatory):

````
$ cat /usr/local/etc/paas-staytus-scripts/config.ini
[DEFAULT]
services = [ 'orchestrator', 'im', 'iam', 'monitoring', 'cpr' ]
LogLevel = INFO
LogPath = /var/log/paasprobe.log

[STAYTUS]
token =
secret =
url =

[service.orchestrator]
name = Orchestrator
url =
path = /info
permalink = orchestrator
issue_status_permalink = unavailable
resolved_status_permalink = running

[service.im]
name = Infrastructure Manager
url =
path = /version
permalink = im
issue_status_permalink = unavailable
resolved_status_permalink = running

[service.iam]
name = IAM
url =
path = /info
permalink = iam
issue_status_permalink = unavailable
resolved_status_permalink = running

[service.monitoring]
name = Monitoring
url =
path = /monitoring/adapters/zabbix/zones/indigo/types/infrastructure/groups
permalink = monitoring
issue_status_permalink = unavailable
resolved_status_permalink = running

[service.cpr]
name = Cloud Provider Ranker
url =
path = /info
permalink = cpr
issue_status_permalink = unavailable
resolved_status_permalink = running
`````

### Run as cron job

Create a cron job in order to run the probe periodically:

````
*/10 * * * * root paas-staytus-health --conf-file /usr/local/etc/paas-staytus-scripts/config.ini
````

The output will be redirected to the log file specified in the configuration file (LogPath parameter in the DEFAULT section) 



