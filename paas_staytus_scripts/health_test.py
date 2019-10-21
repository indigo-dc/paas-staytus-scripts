#!/usr/bin/env python3
#
# File: paas_simple_probe.py
# Author: Marica Antonacci
# Copyright 2019 INFN Bari

from paas_staytus_scripts.staytus import StaytusClient
import requests, json
import configparser, ast, argparse
import logging


def test(staytus, service_conf):
    url = service_conf['url'] + service_conf['path']
    issues = staytus.get_open_issues(service_conf['name'])
    response = requests.get(url)

    logging.info('Response from service {}: {}'.format(service_conf['name'], response.content))

    if response.ok:
       for issue in issues:
          staytus.update_issue(issue['id'], service_conf['resolved_status_permalink'])
    else:
       if not issues:
          logging.warning("Creating new issue for service {}".format(service_conf['permalink']))
          staytus.create_issue(service_conf['name'], service_conf['permalink'], service_conf['issue_status_permalink'], response.text)
      

def main():

    parser = argparse.ArgumentParser(description='Run simple probes on PaaS services.')
    parser.add_argument('--conf-file', required=True, nargs=1, help='the configuration file')
    args = parser.parse_args()

    config_file = args.conf_file

    config = configparser.ConfigParser()
    config.read(config_file)
    basicconf = config['DEFAULT']
    staytusconf = config['STAYTUS']

    loglevel = basicconf['LogLevel']
    logfilename = basicconf['LogPath']
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
       raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level, filename=logfilename, format='%(asctime)s %(levelname)s: %(message)s')

    logging.info("Starting tests...")

    staytus = StaytusClient(staytusconf['url'], staytusconf['token'], staytusconf['secret'])

    for s in ast.literal_eval(config['DEFAULT']['services']):
        key = "service." + s
        try:
          test(staytus, config[key])
        except KeyError as ex:
          logging.error("Service \"{}\" not found in config file. Skipping test...".format(key))

    logging.info("Tests finished.")

if __name__ == "__main__":
    main()
