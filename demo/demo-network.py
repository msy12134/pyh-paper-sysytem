from p4utils.mininetlib.network_API import NetworkAPI
net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.enableCli()

switch_list=['s11','s12','s13','s14','s15','s16','s17','s18','s19']
for i in switch_list:
    net.addP4Switch(i)
host_list=['h11','h12','h13','h14','h15','h16','h17','h18','h19']
for i in host_list:
    net.addHost(i)
for i in switch_list:
    if i!='s15':
        net.setP4Source(i,'demo-controller-switch.p4')
    else:
        net.setP4Source(i,'demo-simple-switch.p4')
net.addLink('s11','s12')
net.addLink('s12','s13')
net.addLink('s14','s15')
net.addLink('s15','s16')
net.addLink('s17','s18')
net.addLink('s18','s19')
net.addLink('s11','s14')
net.addLink('s14','s17')
net.addLink('s12','s15')
net.addLink('s15','s18')
net.addLink('s13','s16')
net.addLink('s16','s19')
zipped=zip(switch_list,host_list)
for i in zipped:
    net.addLink(i[0],i[1])

net.enableCpuPortAll()

net.mixed()
net.enablePcapDumpAll()
net.enableLogAll()
net.startNetwork()