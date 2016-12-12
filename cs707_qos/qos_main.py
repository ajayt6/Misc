'''
User should enter time ranges in 24 hour formats with each set in a different line; in schdeule.txt
Example:
3 - 7
17:30 - 18
21 - 23:50
'''

import subprocess
import getopt
import sys
import schedule
import time


def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print (proc_stdout)

#subprocess_cmd('echo a; echo b')



def start_QOS():
    print("Going to start QOS")
    with open("commands.sh") as commandFile:
        commands = commandFile.read()
        subprocess_cmd(commands)

def stop_QOS():
    print("Going to stop QOS")
    with open("tcDelete.sh") as commandFile:
        commands = commandFile.read()
        subprocess_cmd(commands)

def bandwidth_QOS(threshold):
    '''
    print("bw script to be called")
    Process = subprocess.Popen('bandwidth.sh %s %s' % (str("wlan0"), str("5"),), shell=True,  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(Process.communicate()[0])
    '''
    intf = "wlan0"
    sleep = 5.0

    proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2" % intf,
                            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    rx = float(proc.communicate()[0])

    proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2" % intf,
                            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    tx = float(proc.communicate()[0])

    time.sleep(sleep)

    proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2" % intf,
                            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    rx2 = float(proc.communicate()[0])

    proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2" % intf,
                            shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    tx2 = float(proc.communicate()[0])

    rdiff = (rx2 - rx) / (1024.0 * sleep)
    tdiff = (tx2 - tx) / (1024.0 * sleep)

    print(rdiff, tdiff)
    if tdiff >= float(threshold):
        start_QOS()
    if tdiff < float(threshold):
        stop_QOS()


if __name__ == "__main__":
    threshold = 0
    scheduleFile = "schedule.txt"
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv,"t:s:",["threshold=","schedule="])
    except getopt.GetoptError:
        print ('qos_main.py -t <threshold> -s <schedule file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            threshold = arg
            print ("thres: " + str(threshold))
        elif opt == '-s':
            scheduleFile = arg
            print("schedule: " + str(scheduleFile))

    with open(scheduleFile) as f:
        timeList = f.readlines()
    #schedule.every(10).minutes.do(job)
    #schedule.every().hour.do(job)
    for timeSet in timeList:
        startTime = timeSet.split()[0]
        endTime = timeSet.split()[1]
        schedule.every().day.at(startTime).do(start_QOS)
        schedule.every().day.at(endTime).do(stop_QOS)

    while 1:
        schedule.run_pending()
        #bandwidth_QOS(threshold)
        time.sleep(5)