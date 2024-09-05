from start_method import *

topo = load_topo('/home/mao/Desktop/systerm-code/final/network/topology.json')
domain_1=get_controller_domain("01","05","07","12")
domain_2=get_controller_domain("06","10","07","12")
domain_3=get_controller_domain("01","05","01","06")
domain_4=get_controller_domain("06","10","01","06")
controller_switch_for_domain_1='s00309'
controller_switch_for_domain_2='s00809'
controller_switch_for_domain_3='s00303'
controller_switch_for_domain_4='s00803'

controller_dict=place_controller_for_every_switch(topo)
print(f"交换机控制器数量:{len(controller_dict)}")
make_every_switch_knows_its_CPU_PORT(topo,controller_dict)
switch_to_deviceID_dict=make_every_switch_have_its_own_deviceID(controller_dict)

controller_dict_domain1={}
controller_dict_domain2={}
controller_dict_domain3={}
controller_dict_domain4={}
for i in controller_dict:
    if i in domain_1:
        controller_dict_domain1.update({i:controller_dict[i]})
        implement_ping_between_two_terminals('h'+controller_switch_for_domain_1[1:],'h'+i[1:],controller_dict,topo)
    elif i in domain_2:
        controller_dict_domain2.update({i:controller_dict[i]})
        implement_ping_between_two_terminals('h'+controller_switch_for_domain_2[1:],'h'+i[1:],controller_dict,topo)
    elif i in domain_3:
        controller_dict_domain3.update({i:controller_dict[i]})
        implement_ping_between_two_terminals('h'+controller_switch_for_domain_3[1:],'h'+i[1:],controller_dict,topo)
    elif i in domain_4:
        controller_dict_domain4.update({i:controller_dict[i]})
        implement_ping_between_two_terminals('h'+controller_switch_for_domain_4[1:],'h'+i[1:],controller_dict,topo)
print(f"1:{len(controller_dict_domain1)},2:{len(controller_dict_domain2)},3:{len(controller_dict_domain3)},4:{len(controller_dict_domain4)}")
make_every_switch_knows_its_controller_ipv4(topo.get_host_ip('h'+controller_switch_for_domain_1[1:]),controller_dict_domain1)
make_every_switch_knows_its_controller_ipv4(topo.get_host_ip('h'+controller_switch_for_domain_2[1:]),controller_dict_domain2)
make_every_switch_knows_its_controller_ipv4(topo.get_host_ip('h'+controller_switch_for_domain_3[1:]),controller_dict_domain3)
make_every_switch_knows_its_controller_ipv4(topo.get_host_ip('h'+controller_switch_for_domain_4[1:]),controller_dict_domain4)



print(switch_to_deviceID_dict)
switch_to_deviceID_dict={'s00101': 1, 's00102': 2, 's00103': 3, 's00104': 4, 's00105': 5, 's00106': 6, 's00107': 7, 's00108': 8, 's00109': 9, 's00110': 10, 's00111': 11, 's00112': 12, 's00201': 13, 's00202': 14, 's00203': 15, 's00204': 16, 's00205': 17, 's00206': 18, 's00207': 19, 's00208': 20, 's00209': 21, 's00210': 22, 's00211': 23, 's00212': 24, 's00301': 25, 's00302': 26, 's00304': 27, 's00305': 28, 's00306': 29, 's00307': 30, 's00308': 31, 's00310': 32, 's00311': 33, 's00312': 34, 's00401': 35, 's00402': 36, 's00403': 37, 's00404': 38, 's00405': 39, 's00406': 40, 's00407': 41, 's00408': 42, 's00409': 43, 's00410': 44, 's00411': 45, 's00412': 46, 's00501': 47, 's00502': 48, 's00503': 49, 's00504': 50, 's00505': 51, 's00506': 52, 's00507': 53, 's00508': 54, 's00509': 55, 's00510': 56, 's00511': 57, 's00512': 58, 's00601': 59, 's00602': 60, 's00603': 61, 's00604': 62, 's00605': 63, 's00606': 64, 's00607': 65, 's00608': 66, 's00609': 67, 's00610': 68, 's00611': 69, 's00612': 70, 's00701': 71, 's00702': 72, 's00703': 73, 's00704': 74, 's00705': 75, 's00706': 76, 's00707': 77, 's00708': 78, 's00709': 79, 's00710': 80, 's00711': 81, 's00712': 82, 's00801': 83, 's00802': 84, 's00804': 85, 's00805': 86, 's00806': 87, 's00807': 88, 's00808': 89, 's00810': 90, 's00811': 91, 's00812': 92, 's00901': 93, 's00902': 94, 's00903': 95, 's00904': 96, 's00905': 97, 's00906': 98, 's00907': 99, 's00908': 100, 's00909': 101, 's00910': 102, 's00911': 103, 's00912': 104, 's01001': 105, 's01002': 106, 's01003': 107, 's01004': 108, 's01005': 109, 's01006': 110, 's01007': 111, 's01008': 112, 's01009': 113, 's01010': 114, 's01011': 115, 's01012': 116}
switch_to_deviceID_dict_domain_1={}
switch_to_deviceID_dict_domain_2={}
switch_to_deviceID_dict_domain_3={}
switch_to_deviceID_dict_domain_4={}
for i in switch_to_deviceID_dict:
    if i in domain_1:
        switch_to_deviceID_dict_domain_1.update({i:switch_to_deviceID_dict[i]})
    elif i in domain_2:
        switch_to_deviceID_dict_domain_2.update({i:switch_to_deviceID_dict[i]})
    elif i in domain_3:
        switch_to_deviceID_dict_domain_3.update({i:switch_to_deviceID_dict[i]})
    elif i in domain_4:
        switch_to_deviceID_dict_domain_4.update({i:switch_to_deviceID_dict[i]})
for i in controller_dict:
    sniff_port_name=i+"-cpu-eth1"
    if i in domain_1:
        mycontroller(sniff_port_name,controller_dict[i],switch_to_deviceID_dict_domain_1,topo,1).start_receiving_cpu_packet()
    if i in domain_2:
        mycontroller(sniff_port_name,controller_dict[i],switch_to_deviceID_dict_domain_2,topo,2).start_receiving_cpu_packet()
    if i in domain_3:
        mycontroller(sniff_port_name,controller_dict[i],switch_to_deviceID_dict_domain_3,topo,3).start_receiving_cpu_packet()
    if i in domain_4:
        mycontroller(sniff_port_name,controller_dict[i],switch_to_deviceID_dict_domain_4,topo,4).start_receiving_cpu_packet()
    