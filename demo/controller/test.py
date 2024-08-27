from p4utils.utils.helper import load_topo
topo = load_topo('/home/mao/Desktop/systerm-code/demo/network/topology.json')
print(type(topo.get_host_name("10.0.5.15")))
print(topo.get_shortest_paths_between_nodes("s11","h15")[0])
print(topo.get_host_ip)