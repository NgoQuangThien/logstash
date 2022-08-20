import os
import yaml
import subprocess


def get_hosts():
    cmd = "sudo salt-call pillar.get 'logstash:nodes'"
    cmd_result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = cmd_result.stdout.read().decode('utf-8').replace('-', '')
    hosts = yaml.load(stdout)['local']
    hosts_ip = list()
    if 'receiver' in hosts.keys():
        for host in hosts['receiver']:
            hosts_ip.append(hosts['receiver'][host]['ip'])
    else:
        for host in hosts['manager']:
            hosts_ip.append(hosts['manager'][host]['ip'])
    return str(hosts_ip)


def render_configuration(hosts):
    config = """output {
    redis {
        host => %s
        port => 6379
        data_type => 'list'
        key => 'logstash:unparsed'
        congestion_interval => 1
        congestion_threshold => 50000000
        batch => true
        batch_events => 125
    }
}""" %(hosts)
    return config


def create_file_config(config):
    for folder in next(os.walk('pipeline'))[1]:
        file_path = 'pipeline' + '/' + folder + '/' + 'output_redis.conf'
        with open(file_path, 'w') as f:
            f.write(config)


hosts = get_hosts()
config = render_configuration(hosts)
create_file_config(config)
