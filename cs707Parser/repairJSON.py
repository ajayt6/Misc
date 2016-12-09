import re
import json

invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)
import os
#rootdir = 'E:\\programBase\\wireshark\\sniffer\\wireless\\nov15'
input_direcory = 'E:\\programBase\\wireshark\\sniffer\\wireless\\outputJSON'
output_directory = 'E:\\programBase\\wireshark\\sniffer\\wireless\\repairedJSON'

for subdir, dirs, files in os.walk(input_direcory):
    for file in files:
        input_json_file = os.path.join(input_direcory, file)
        output_json_file = os.path.join(output_directory, file)
        with open(input_json_file, 'r') as myfile:

            data=myfile.read()
            print(data[0:50])
            newData = data.replace(",","",1)
            print(newData[0:50])
            f = open(output_json_file.replace(".cap",""), 'w')  # opens file with name of "test.txt"

            f.write(newData)
            f.close()
            #json.loads(repair(data))