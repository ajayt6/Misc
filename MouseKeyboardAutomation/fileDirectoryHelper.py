import os
rootdir = 'E:\\programBase\\wireshark\\sniffer\\wireless\\nov15'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print (os.path.join(subdir, file))