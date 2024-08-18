from p4utils.mininetlib.network_API import NetworkAPI
import pandas as pd

file_path = 'net.csv'
adjacency_matrix = pd.read_csv(file_path)
long_format = adjacency_matrix.melt(id_vars=['satellite'], var_name='satellite2', value_name='distance')
long_format = long_format[long_format['distance'] != 0]
long_format.reset_index(drop=True, inplace=True)

long_format['satellite_pair'] = long_format.apply(lambda row: tuple(sorted([row['satellite'], row['satellite2']])),axis=1)
long_format = long_format.drop_duplicates(subset=['satellite_pair'])
result = long_format.drop(columns=['satellite_pair'])
result.reset_index(drop=True, inplace=True)

def convert_name(name):
    return 's'+name[-5:]
result['satellite'] = result['satellite'].apply(convert_name)
result['satellite2'] = result['satellite2'].apply(convert_name)

numbers1 = []
for i in range(1, 11):
    numbers1.append(f"{i:02}")
numbers2 = []
for i in range(1, 13):
    numbers2.append(f"{i:02}")



net = NetworkAPI()

# Network general options
net.setLogLevel('info')
net.enableCli()

for i in range(0,10):
    for j in range(0,12):
        net.addP4Switch('s0'+numbers1[i]+numbers2[j])

for index,row in result.iterrows():
    satellite = row['satellite']
    satellite2 = row['satellite2']
    Delay= row['distance']/300000*1000
    net.addLink(satellite,satellite2)
    net.setDelay(satellite,satellite2,Delay)

    
net.mixed()

net.enablePcapDumpAll()
net.enableLogAll()

net.startNetwork()
