from scapy.all import Packet,IPField,BitField,bind_layers,MACField
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP


class request_t(Packet):
    name="request"
    fields_desc=[
        BitField('deviceid',0,8),
        IPField('dst_addr','0.0.0.0')
    ]

class response_t(Packet):
    name="response"
    fields_desc=[
        BitField('deviceid',0,8),
        IPField('dst_addr','0.0.0.0'),
        BitField('port',0,9),
        MACField('dst_port_mac',"00:00:00:00:00:00"),
        BitField('padding',0,7)
    ]

bind_layers(Ether,IP)