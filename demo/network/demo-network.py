from p4utils.mininetlib.network_API import NetworkAPI
net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.enableCli()
#设置拓扑硬件配置
switch_list=['s11','s12','s13','s14','s15','s16','s17','s18','s19']
for i in switch_list:
    net.addP4Switch(i)
host_list=['h11','h12','h13','h14','h15','h16','h17','h18','h19']
for i in host_list:
    net.addHost(i)
#每个交换机设置相应p4程序
net.setP4Source("s15",'demo-controller-switch.p4')
for i in ['s11','s12','s13','s14','s16','s17','s18','s19']:
    filename=i+".p4"
    net.setP4Source(i,filename)
#设置连接
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