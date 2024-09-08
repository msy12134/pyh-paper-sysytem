from scapy.all import sniff,Packet
import threading
import deal_packet
from scapy.layers.inet import IP
from scapy.all import sendp
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
from p4utils.utils.topology import NetworkGraph
import requests
import websockets
import asyncio
class mycontroller:
    def __init__(self,sniff_port:str,controller:SimpleSwitchThriftAPI,deviceid_switchname_dict:dict,topo:NetworkGraph,domainid:int):
        self.sniff_port=sniff_port
        self.controller=controller
        self.deviceid_switchname_dict=deviceid_switchname_dict
        self.topo=topo
        self.domainid=domainid
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
                print(f"该目的ipv4地址超出了自治域范围,向OCC询问信息")
                """
                第一种情况：
                如果单纯就是涉及到了跨域的通信，控制器向OCC构造一个请求获取流表信息，控制器将接收到的流表信息推送给对应的交换机，从而实现跨域通信
                第二种情况：
                预缓存就先不在这里写了，到时候直接写个命令行程序去调后端的服务就行
                """
                response=requests.get(f"http://127.0.0.1:8000/{self.domainid}/from/{dict['deviceid']}/to/{dict['dst_addr']}")
                table_info_for_each_switch=response.json()
                print(f"接收到的OCC响应信息如下：{table_info_for_each_switch}")
                for i in table_info_for_each_switch:
                    response_packet=deal_packet.make_a_response_packet(**table_info_for_each_switch[i])
                    sendp(response_packet,iface=self.sniff_port)
            else:
                hostname=self.topo.get_host_name(str(dict["dst_addr"]))
                route=self.topo.get_shortest_paths_between_nodes(switch_name,hostname)[0]#('s1','s2','s3','h1')
                for i in range(len(route)-1):
                    port=self.topo.node_to_node_port_num(route[i],route[i+1])
                    ipv4dst=self.topo.get_host_ip('h'+route[i][1:])
                    mac=self.topo.node_to_node_mac(route[i+1],route[i])
                    deviceid=int(self.deviceid_switchname_dict[route[i]])
                    dst_addr=str(self.topo.get_host_ip(route[-1]))
                    response=deal_packet.make_a_response_packet(int(deviceid),dst_addr,int(port),mac,str(ipv4dst))
                    sendp(response,iface=self.sniff_port)
    async def websocket_client(self):
        url = "ws://localhost:8000/ws/1"
        while True:
            async with websockets.connect(url) as websocket:
                await websocket.send("hello server")
                response=await websocket.recv()  
                print(f"receive from server {response}")

              
    