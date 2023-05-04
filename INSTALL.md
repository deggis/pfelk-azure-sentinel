# PfELK->Sentinel Install instructions

Note: instructions focus on firewall logs, as that's currently only item
there's a Sentinel ASIM parser for.

![architecture](pfelk-azure-sentinel-architecture2.png)

## Before you begin: Alternatives

Before you begin: An alternative approach for connecting pfsense logs to Sentinel is to use Rsyslog. PfSense -> Rsyslog -> CEF (CommonEventFormat), documented [here](https://github.com/Azure/Azure-Sentinel/tree/master/DataConnectors/pfsense).

If you'd rather use Logstash, then this guide might be for you.

## PfSense

1. Configure remote logging with syslog e.g. using [Netgate's guide](https://docs.netgate.com/pfsense/en/latest/monitoring/logs/remote.html)
2. Point logs to your Logstash

## Logstash (with PfELK conf)

For setting up Logstash, check [PfELK project](https://github.com/pfelk/pfelk).

For setting up the output towards Sentinel, check [in.security's post](https://in.security/2022/11/28/logstash-sentinel-round-two/).

The needed part here is the Logstash and its configuration. Main bits of the configuration are:

- syslog input for PfSense [01-inputs.pfelk](Logstash-Configuration/etc/logstash/conf.d/01-inputs.pfelk)
- remove type column [49-cleanup.pfelk](Logstash-Configuration/etc/logstash/conf.d/49-cleanup.pfelk)
- output to Azure Monitor [50-outputs.pfelk](Logstash-Configuration/etc/logstash/conf.d/50-outputs.pfelk)

If you already use PfELK, you only need to add output plugin and add a mutator for "type" column. Otherwise, you need a Logstash installation.

Note that Azure Log Analytics Workspace and Azure Sentinel is priced by the ingested data volume. Currently first month is free, and you can have up to 20 free trials per tenant [Azure Sentinel pricing](https://azure.microsoft.com/en-us/pricing/details/microsoft-sentinel/).

## From Logstash to custom Log Analytics table via Azure Monitor

Logstash -> Azure Monitor (DCE, DCR) -> Custom table in Log Analytics workspace.

Check this part from [in.security's post](https://in.security/2022/11/28/logstash-sentinel-round-two/).

When prompted for table name, use `PfELK`. This results to `PfELK_CL` table and data stream `Custom-PfELK_CL`.

## Sentinel transformations

When logs flow to a table in a Log Analytics Workspace, they can be queried using KQL.

Note that:
 - the data not in the raw PfSense syslog format anymore, so existing PfSense KQL parsers don't work. I also didn't find any, which lead to working on this repo.
 - the data format is not the same as in [noodlemctwoodle's repo](https://github.com/noodlemctwoodle/pf-azure-sentinel)
   - I don't actually know why this is. In noodlemctwoodle's docs the data is in many `..._s` columns.
   - In any case, the KQL queries at [noodlemctwoodle's repo](https://github.com/noodlemctwoodle/pf-azure-sentinel/tree/main/KQL/pfSense/Queries) should not work directly.
   - the data is not in CommonEventFormat
 
![schema](pfelk_data_schema.png)
