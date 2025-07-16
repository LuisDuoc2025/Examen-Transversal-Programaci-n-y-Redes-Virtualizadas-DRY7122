from ncclient import manager
import xml.dom.minidom

m = manager.connect(
    host="192.168.56.111",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
    ) 

# Cambiar hostname al router con los apellidos del grupo
netconf_hostname = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>Contreras-Gutierrez</hostname>
  </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_hostname)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

# Crear interfaz Loopback11
netconf_loopback11 = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>11</name>
    <description>NETCONF Loopback 11</description>
    <ip>
     <address>
      <primary>
       <address>11.11.11.11</address>
       <mask>255.255.255.255</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""
netconf_reply = m.edit_config(target="running", config=netconf_loopback11)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
