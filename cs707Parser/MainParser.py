import json
from pprint import pprint
import csv

with open('ByPortJSON.json') as data_file:
    data = json.load(data_file)

friendOfBro = {}
proof = {}

csv_file = 'friendOfBroCSV.csv'

for packet in data:
    try:
        packetData = packet["_source"]["layers"]["data"]["data.data"].replace(':','')
        packetDataASCII = bytearray.fromhex(packetData).decode()
        epochTimeOfData = float(packet["_source"]["layers"]["frame"]["frame.time_epoch"])

        if packetDataASCII in friendOfBro:
            friendOfBro[packetDataASCII] = epochTimeOfData - friendOfBro[packetDataASCII]
        else:
            friendOfBro[packetDataASCII] = epochTimeOfData

        if packetDataASCII in proof:
            proof[packetDataASCII] = 1 + proof[packetDataASCII]
        else:
            proof[packetDataASCII] = 1


    except:
        print("") #Ignore. Not packet with data info")

'''
for packet in  friendOfBro:
    print('key: ' + packet + '; value: '+ str(friendOfBro[packet]))
'''

i=0
for packet in  proof:
    print('key: ' + packet + '; value: ' + str(proof[packet]))
    if (proof[packet] !=2 ):
        i=i+1
print('Number of mutant instances: '+ str(i))

with open(csv_file, 'w') as csv_file:
    writer = csv.writer(csv_file,delimiter=' ', lineterminator='\n')
    for key, value in friendOfBro.items():
        writer.writerow([key, value])


#pprint(data[0])
#pprint(data[0]["_source"]["layers"]["data"]["data.data"])
#pprint(data[0]["_source"]["layers"]["frame"]["frame.time_epoch"])