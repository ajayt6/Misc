import json
from pprint import pprint
import csv
import os
import collections
import traceback

input_direcory = 'E:\\programBase\\wireshark\\sniffer\\wireless\\repairedJSON'
output_directory = 'E:\\programBase\\wireshark\\sniffer\\wireless\\repairedJSON'
csv_file = 'E:\\programBase\\wireshark\\sniffer\\wireless\\outputJSON\\T1_OT2CSV_nov30Stress.csv'
output_txt_file = "E:\\programBase\\wireshark\\sniffer\\wireless\\outputJSON\\T1_OT2txt_Dec6_noRulesRe.txt"

T1_OT2CSV = collections.OrderedDict()
for subdir, dirs, files in os.walk(input_direcory):
    for file in files:
        input_file = os.path.join(input_direcory,file)
        with open(input_file) as data_file:
            print("Going to load data file" + str(file))
            try:
                data = json.load(data_file)


                proof = {}



                for packet in data:
                    try:
                        packetData = packet["_source"]["layers"]["data"]["data.data"].replace(':','')
                        packetDataASCII = bytearray.fromhex(packetData).decode()
                        epochTimeOfData = str(packet["_source"]["layers"]["frame"]["frame.time_epoch"])


                        #print("here")
                        if packetDataASCII in T1_OT2CSV:
                            #print("before diff")
                            diff = float(epochTimeOfData) - float(T1_OT2CSV[packetDataASCII])
                            #print("before tuple assignment")
                            tuplePair = T1_OT2CSV[packetDataASCII], diff
                            T1_OT2CSV[packetDataASCII] = tuplePair
                            #print("The tuple pair is: " + tuplePair[0] + " " + str(tuplePair[1]) )
                        else:
                            #print("In else")
                            T1_OT2CSV[packetDataASCII] = epochTimeOfData
                            #if packetDataASCII in T1_OT2CSV:
                             #   print("yeah key present")

                        if packetDataASCII in proof:
                            proof[packetDataASCII] = 1 + proof[packetDataASCII]
                        else:
                            proof[packetDataASCII] = 1
                        '''
                        if "Sent," + packetDataASCII in T1_OT2CSV:
                            T1_OT2CSV["Recd " + packetDataASCII] = epochTimeOfData
                        else:
                            T1_OT2CSV["Sent " + packetDataASCII] = epochTimeOfData

                        if packetDataASCII in proof:
                            proof[packetDataASCII] = 1 + proof[packetDataASCII]
                        else:
                            proof[packetDataASCII] = 1
                        '''


                    except:
                        #traceback.print_exc()
                        print("",end="") #Ignore. Not packet with data info")
            except:
                print("Error in json decode")

'''
for packet in  friendOfBro:
    print('key: ' + packet + '; value: '+ str(friendOfBro[packet]))



i=0
for packet in  proof:
    print('key: ' + packet + '; value: ' + str(proof[packet]))
    if (proof[packet] !=2 ):
        i=i+1
print('Number of mutant instances: '+ str(i))
'''
'''
print("Going to start writing to csv")
with open(csv_file, 'w',encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file,delimiter=' ', lineterminator='\n')
    for key, value in T1_OT2CSV.items():
        writer.writerow([key, value])
'''
print("Going to start writing to comma separated text file")
with open(output_txt_file, 'w') as myfile:
    for key,value in T1_OT2CSV.items():
        #print("key: " + key + " value: " + value)
        try:
            pairFirst,pairSecond = value
            pairSecond = int(pairSecond * 1000)
            myfile.write(key + "," + pairFirst + "," + str(pairSecond)+"\n")
        except:
            print("",end="")#print("error")
            traceback.print_exc()

#pprint(data[0])
#pprint(data[0]["_source"]["layers"]["data"]["data.data"])
#pprint(data[0]["_source"]["layers"]["frame"]["frame.time_epoch"])