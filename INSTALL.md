# Install instructions

Note: instructions focus on firewall logs, as that's currently only item
there's a Sentinel ASIM parser for.

![architecture](pfelk-azure-sentinel-architecture2.png)

## PfSense

1. Configure remote logging with syslog e.g. using [Netgate's guide](https://docs.netgate.com/pfsense/en/latest/monitoring/logs/remote.html)
2. Point logs to your Logstash

## PfELK / Logstash

For setting up Logstash, check [PfELK project](https://github.com/pfelk/pfelk).

For setting up the output towards Sentinel, check [in.security's post](https://in.security/2022/11/28/logstash-sentinel-round-two/).

The needed part here is the Logstash and its configuration. Main bits of the configuration are:

- syslog input for PfSense [01-inputs.pfelk](Logstash-Configuration/etc/logstash/conf.d/01-inputs.pfelk)
- remove type column [49-cleanup.pfelk](Logstash-Configuration/etc/logstash/conf.d/49-cleanup.pfelk)
- output to Azure Monitor [50-outputs.pfelk](Logstash-Configuration/etc/logstash/conf.d/50-outputs.pfelk)

If you already use PfELK, you only need to add output plugin and add a mutator for "type" column. Otherwise, you need a Logstash installation.

## To custom Log Analytics table via Azure Monitor

Logstash -> Azure Monitor -> Custom table

Check this part from [in.security's post](https://in.security/2022/11/28/logstash-sentinel-round-two/).

