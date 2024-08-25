from p4utils.utils.helper import load_topo
from p4utils.utils.sswitch_thrift_API import SimpleSwitchThriftAPI


#为每一个交换机添加一个控制器
def place_controller_for_every_switch(topo):
    """为拓扑中的每个交换机设置一个关联的控制器.

    Args:
        topo: load_topo(拓扑json文件的具体路径)方法的返回对象

    Returns:
        dict:字典中的键是每个交换机的名称，字典的值是对应交换机的控制器对象
    """
    switch_name_list=list(topo.get_p4switches().keys())
    switch_thrift_port_list=[topo.get_thrift_port(i) for i in switch_name_list]
    print(switch_thrift_port_list)
    controller_dict={}
    for i in list(zip(switch_name_list,switch_thrift_port_list)):
        controller_dict[i[0]]=SimpleSwitchThriftAPI(int(i[1]))
    return controller_dict
    

#在部署完相应的p4程序添加转发流表，让两个终端自动ping通
def implement_ping_between_two_terminals(host1,host2,dict,topo):
    """使得拓扑中的host1主机和host2主机可以ping通.

    Args:
        host1(str): 终端1的名称
        host2(str): 终端2的名称
        dict(dict): place_controller_for_every_switch方法的返回对象
        topo: load_topo(拓扑json文件的具体路径)方法的返回对象

    Returns:
        None: 
    """
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
        print(f"交换机{route[i]}的流表初始化完成,可以和域内控制器ping通")


def make_every_switch_knows_its_CPU_PORT(topo,dict):
    """使得每个交换机都配置查找cpu port的流表项（每个交换机只有一条）.

    Args:
        topo: load_topo(拓扑json文件的具体路径)方法的返回对象
        dict(dict): place_controller_for_every_switch方法的返回对象
    
    Returns:
        None: 
    """
    switch_name_list=list(topo.get_p4switches().keys())
    switch_cpu_port=[topo.get_cpu_port_index(i) for i in switch_name_list]
    dict_switchname_to_cpuport={i[0]:i[1] for i in list(zip(switch_name_list,switch_cpu_port))}
    for i in dict:
        dict[i].table_add('set_cpu_port_for_this_packet','set_cpu_port',["0x0800"],[str(dict_switchname_to_cpuport[i])])

if __name__=='__main__':
    topo = load_topo('/home/mao/Desktop/systerm-code/demo/network/topology.json')
    controller_dict=place_controller_for_every_switch(topo)
    make_every_switch_knows_its_CPU_PORT(topo,controller_dict)
    implement_ping_between_two_terminals("h11","h19",controller_dict,topo)

