from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


#为每一个交换机添加一个控制器
def place_controller_for_every_switch(topo):
    switch_name_list=list(topo.get_p4switches().keys())
    switch_thrift_port_list=[topo.get_thrift_port(i) for i in switch_name_list]
    print(switch_thrift_port_list)
    controller_dict={}
    for i in list(zip(switch_name_list,switch_thrift_port_list)):
        controller_dict[i[0]]=SimpleSwitchThriftAPI(int(i[1]))
    return controller_dict
    

#在部署完相应的p4程序后让两个终端自动ping通
def implement_ping_between_two_terminals(host1,host2,dict,topo):
    route=topo.get_shortest_paths_between_nodes(host1,host2)[0]
    # print(route)
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
    print(f"交换机{route[i]}的流表初始化完成,可以和域内控制器ping通")

if __name__=='__main__':
    topo = load_topo('/home/mao/Desktop/systerm-code/final/network/topology.json')
    controller_dict=place_controller_for_every_switch(topo)
    implement_ping_between_two_terminals("h00309","h00803",controller_dict,topo)


