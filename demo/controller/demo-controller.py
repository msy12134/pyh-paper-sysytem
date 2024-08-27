from scapy.all import sniff
import threading
import deal_packet
from scapy.layers.inet import IP
from scapy.all import sendp
class mycontroller:
    def __init__(self,sniff_port,controller,deviceid_switchname_dict,topo):
        self.sniff_port=sniff_port
        self.controller=controller
        self.deviceid_switchname_dict=deviceid_switchname_dict
        self.topo=topo
    def start_receiving_cpu_packet(self):
        sniff_thread=threading.Thread(target=self.__sniff_packet)
        sniff_thread.daemon=True
        sniff_thread.start()
        print(f"网络端口{self.sniff_port}开始在后台监听cpu数据包")

    def __sniff_packet(self):
        sniff(iface=self.sniff_packet,prn=self.__packet_deal)

    def __packet_deal(self,packet):
        if packet[IP].proto==151:  #普通交换机收到response数据包直接插表
            dict=deal_packet.deal_packet_for_simple_switch(packet)
            self.controller.table_add("ipv4_lpm",'ipv4_forward',[str(dict["dst_addr"])],[str(dict["dst_port_mac"]),str(dict["port"])])
            self.controller.table_add("ipv4_dst_memory",'ipv4_forward',[str(dict["dst_addr"])],[str(dict["dst_port_mac"])])
        elif packet[IP].proto==150: #控制交换机收到request数据包解析请求，构造response
            dict=deal_packet.deal_packet_for_controller_switch(packet)
            for i in self.deviceid_switchname_dict:
                if self.deviceid_switchname_dict[i]==dict["deviceid"]:
                    switch_name=i
                    break
            hostname=self.topo.get_host_name(str(dict["dst_addr"]))
            route=self.topo.get_shortest_paths_between_nodes(switch_name,hostname)[0]
            port=self.topo.node_to_node_port_num(route[0],route[1])
            ipv4dst=self.topo.get_host_ip('h'+switch_name[1:])
            mac=self.topo.node_to_node_mac(route[1],route[0])
            response=deal_packet.make_a_response_packet(int(dict["deviceid"]),str(dict["dst_addr"]),int(port),str(mac),str(ipv4dst))
            sendp(response,iface=self.sniff_port,)


    