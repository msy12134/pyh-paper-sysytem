from fastapi import FastAPI
from ipaddress import IPv4Address
from p4utils.utils.topology import NetworkGraph
from p4utils.utils.helper import load_topo
import uvicorn
each_switch_and_its_switchid_dict={'s00101': 1, 's00102': 2, 's00103': 3, 's00104': 4, 's00105': 5, 's00106': 6, 's00107': 7, 's00108': 8, 's00109': 9, 's00110': 10,
                          's00111': 11, 's00112': 12, 's00201': 13, 's00202': 14, 's00203': 15, 's00204': 16, 's00205': 17, 's00206': 18, 's00207': 19, 's00208': 20, 
                          's00209': 21, 's00210': 22, 's00211': 23, 's00212': 24, 's00301': 25, 's00302': 26, 's00304': 27, 's00305': 28, 's00306': 29, 's00307': 30, 
                          's00308': 31, 's00310': 32, 's00311': 33, 's00312': 34, 's00401': 35, 's00402': 36, 's00403': 37, 's00404': 38, 's00405': 39, 's00406': 40, 
                          's00407': 41, 's00408': 42, 's00409': 43, 's00410': 44, 's00411': 45, 's00412': 46, 's00501': 47, 's00502': 48, 's00503': 49, 's00504': 50, 
                          's00505': 51, 's00506': 52, 's00507': 53, 's00508': 54, 's00509': 55, 's00510': 56, 's00511': 57, 's00512': 58, 's00601': 59, 's00602': 60, 
                          's00603': 61, 's00604': 62, 's00605': 63, 's00606': 64, 's00607': 65, 's00608': 66, 's00609': 67, 's00610': 68, 's00611': 69, 's00612': 70, 
                          's00701': 71, 's00702': 72, 's00703': 73, 's00704': 74, 's00705': 75, 's00706': 76, 's00707': 77, 's00708': 78, 's00709': 79, 's00710': 80, 
                          's00711': 81, 's00712': 82, 's00801': 83, 's00802': 84, 's00804': 85, 's00805': 86, 's00806': 87, 's00807': 88, 's00808': 89, 's00810': 90,
                          's00811': 91, 's00812': 92, 's00901': 93, 's00902': 94, 's00903': 95, 's00904': 96, 's00905': 97, 's00906': 98, 's00907': 99, 's00908': 100, 
                          's00909': 101, 's00910': 102, 's00911': 103, 's00912': 104, 's01001': 105, 's01002': 106, 's01003': 107, 's01004': 108, 's01005': 109, 
                          's01006': 110, 's01007': 111, 's01008': 112, 's01009': 113, 's01010': 114, 's01011': 115, 's01012': 116}
def get_controller_domain(x_from:str,x_to:str,y_from:str,y_to:str):
    """.

    Args:
        
    Returns:
        list[str]: 字典的键是交换机的名字，对应的值是每个交换机的deviceID 
    """
    domain=['s0'+str(x).zfill(2)+str(y).zfill(2) for x in range(int(x_from),int(x_to)+1) for y in range(int(y_from),int(y_to)+1)]
    return domain
domain_1=get_controller_domain("01","05","07","12")
domain_2=get_controller_domain("06","10","07","12")
domain_3=get_controller_domain("01","05","01","06")
domain_4=get_controller_domain("06","10","01","06")
topo = load_topo('/home/mao/Desktop/systerm-code/final/network/topology.json')
app=FastAPI()
domain_dict={"1":domain_1,"2":domain_2,"3":domain_3,"4":domain_4}


@app.get("/{domainid}/from/{deviceid}/to/{ip_address}")
def query_the_path_info(domainid:str,deviceid:int,ip_address:IPv4Address):
    destination_hostname=topo.get_host_name(str(ip_address))
    reversed_each_switch_and_its_switchid_dict={a:b for b,a in each_switch_and_its_switchid_dict.items()}
    the_query_device_name=reversed_each_switch_and_its_switchid_dict[deviceid]
    print(f"{domainid}想知道其中的{the_query_device_name}交换机去往{destination_hostname}的路径")
    route=topo.get_shortest_paths_between_nodes(the_query_device_name,destination_hostname)[0]
    print(f"OCC找到了最短路径：{route},开始构造路由表信息")
    table_entry_for_each_switch={}
    for i in range(len(route)-1):
        table_entry_info={}
        deviceid=each_switch_and_its_switchid_dict[route[i]]
        dst_addr=topo.get_host_ip(route[-1])
        port=topo.node_to_node_port_num(route[i],route[i+1])
        mac=topo.node_to_node_mac(route[i+1],route[i])
        ipv4dst=topo.get_host_ip("h"+route[i][1:])
        table_entry_info={"deviceid":int(deviceid),"dst_addr":str(dst_addr),"port":int(port),
                          "dst_port_mac":mac,"ipv4":str(ipv4dst)}
        table_entry_for_each_switch[route[i]]=table_entry_info
    print(f"构造的路由信息：{table_entry_for_each_switch}")
    return {key:value for key,value in table_entry_for_each_switch.items() if key in domain_dict[domainid]}

if __name__=="__main__":
    uvicorn.run(app)
    