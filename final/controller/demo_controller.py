from scapy.all import sniff,Packet
import threading
import deal_packet
from scapy.layers.inet import IP
from scapy.all import sendp
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from p4utils.utils.topology import NetworkGraph
class mycontroller:
    def __init__(self,sniff_port:str,controller:SimpleSwitchThriftAPI,deviceid_switchname_dict:dict,topo:NetworkGraph):
        self.sniff_port=sniff_port
        self.controller=controller
        self.deviceid_switchname_dict=deviceid_switchname_dict
        self.topo=topo
    def start_receiving_cpu_packet(self):
        sniff_thread=threading.Thread(target=self.__sniff_packet)
        sniff_thread.start()
        print(f"网络端口{self.sniff_port}开始在后台监听cpu数据包")

    def __sniff_packet(self):
        sniff(iface=self.sniff_port,prn=self.__packet_deal)
        
    def __packet_deal(self,packet:Packet):
        print(f"{self.sniff_port[0:6]}的CPUport收到数据包")
        # packet.show()
        if packet[IP].proto==151:  #普通交换机收到response数据包直接插表
            dict=deal_packet.deal_packet_for_simple_switch(packet)
            mac_int=dict["dst_port_mac"] #这时得到的mac地址是一个int类型的
            mac_hex = f'{mac_int:012x}'  # 转换为 12 位的十六进制数
            mac_str = ':'.join(mac_hex[i:i+2] for i in range(0, 12, 2))
            self.controller.table_add("ipv4_lpm",'ipv4_forward',[str(dict["dst_addr"])],[mac_str,str(dict["port"])])
            self.controller.table_add("ipv4_dst_memory",'ipv4_forward',[str(dict["dst_addr"])],[mac_str,str(dict["port"])])
        elif packet[IP].proto==150: #控制交换机收到request数据包解析请求，构造response
            dict=deal_packet.deal_packet_for_controller_switch(packet)
            for i in self.deviceid_switchname_dict:
                if self.deviceid_switchname_dict[i]==dict["deviceid"]:
                    switch_name=i
                    break
            print(self.topo.get_host_name(dict["dst_addr"]))
            if 's'+self.topo.get_host_name(dict["dst_addr"])[1:] not in self.deviceid_switchname_dict:
                print(f"该目的ipv4地址超出了自治域范围")
            else:
                hostname=self.topo.get_host_name(str(dict["dst_addr"]))
                route=self.topo.get_shortest_paths_between_nodes(switch_name,hostname)[0]
                port=self.topo.node_to_node_port_num(route[0],route[1])
                ipv4dst=self.topo.get_host_ip('h'+switch_name[1:])
                mac=self.topo.node_to_node_mac(route[1],route[0])
                response=deal_packet.make_a_response_packet(int(dict["deviceid"]),str(dict["dst_addr"]),int(port),mac,str(ipv4dst))
                sendp(response,iface=self.sniff_port)

    