from p4utils.mininetlib.network_API import NetworkAPI
net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.enableCli()


net.addP4Switch('s11')
net.addP4Switch('s12')
net.addP4Switch('s13')
net.addP4Switch('s14')
net.addP4Switch('s15')
net.addP4Switch('s16')
net.addP4Switch('s17')
net.addP4Switch('s18')
net.addP4Switch('s19')

net.setP4Source('s11','demo-simple-switch.p4')
net.setP4Source('s12','demo-simple-switch.p4')
net.setP4Source('s13','demo-simple-switch.p4')
net.setP4Source('s14','demo-simple-switch.p4')
net.setP4Source('s15','demo-controller-switch.p4')
net.setP4Source('s16','demo-simple-switch.p4')
net.setP4Source('s17','demo-simple-switch.p4')
net.setP4Source('s18','demo-simple-switch.p4')
net.setP4Source('s19','demo-simple-switch.p4')

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

net.enableCpuPortAll()

net.mixed()
net.enablePcapDumpAll()
net.enableLogAll()
net.startNetwork()