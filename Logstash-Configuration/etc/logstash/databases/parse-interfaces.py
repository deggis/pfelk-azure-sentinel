import xml.etree.ElementTree as ET

# Take <interfaces> section of the
# PfSense XML configuration dump
# (including the tag <interfaces>)

with open('interfaces_pfsense.txt') as in_f:
    xml_string = in_f.read()
    root = ET.fromstring(xml_string)

    print('"iface_id","iface_description","iface_ip"')
    for iface_elem in root.findall('./'):
        if_id = iface_elem.find('./if').text
        descr_val = iface_elem.find('./descr').text
        ipaddr_elem = iface_elem.find('./ipaddr')
        ipaddr_val = ipaddr_elem.text if (ipaddr_elem is not None) else ''
        subnet_elem = iface_elem.find('./subnet')
        subnet = subnet_elem.text if (subnet_elem is not None) else ''
        print(f"""\"{if_id}","{descr_val}","{ipaddr_val}/{subnet}\"""")