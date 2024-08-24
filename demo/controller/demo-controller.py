from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI
topo = load_topo('/home/mao/Desktop/systerm-code/demo/network/topology.json')

s11=SimpleSwitchThriftAPI(9090)
s12=SimpleSwitchThriftAPI(9091)
s13=SimpleSwitchThriftAPI(9092)
s14=SimpleSwitchThriftAPI(9093)
s15=SimpleSwitchThriftAPI(9094)
s16=SimpleSwitchThriftAPI(9095)
s17=SimpleSwitchThriftAPI(9096)
s18=SimpleSwitchThriftAPI(9097)
s19=SimpleSwitchThriftAPI(9098)
dict={"s11":s11,"s12":s12,"s13":s13,"s14":s14,"s15":s15,
      "s16":s16,"s17":s17,"s18":s18,"s19":s19}

def implement_ping_between_two_terminals(host1,host2):
    route=topo.get_shortest_paths_between_nodes(host1,host2)[0]
    print(route)
    host1_ip,host2_ip=topo.get_host_ip(host1),topo.get_host_ip(host2)
    for i in range(1,len(route)-1):
        port_right=topo.node_to_node_port_num(route[i],route[i+1])
        mac_right=topo.node_to_node_mac(route[i+1],route[i])
        mac_left=topo.node_to_node_mac(route[i-1],route[i])
        port_left=topo.node_to_node_port_num(route[i],route[i-1])
        dict[route[i]].table_add('ipv4_lpm','ipv4_forward',[host2_ip],[mac_right,str(port_right)])
        dict[route[i]].table_add('ipv4_lpm','ipv4_forward',[host1_ip],[mac_left,str(port_left)])
        dict[route[i]].table_add('ipv4_dst_memory','ipv4_forward',[host2_ip],[mac_right,str(port_right)])
        dict[route[i]].table_add('ipv4_dst_memory','ipv4_forward',[host1_ip],[mac_right,str(port_left)])
        print(f"交换机{route[i]}的流表初始化完成")

if __name__=='__main__':
    implement_ping_between_two_terminals('h11','h15')
    implement_ping_between_two_terminals('h12','h15')
    implement_ping_between_two_terminals('h13','h15')
    implement_ping_between_two_terminals('h14','h15')
    


