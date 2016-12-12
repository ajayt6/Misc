# responsible for coordinating schedules between clients
import subprocess, time


intf = "wlan0"
sleep = 5.0

proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2" % intf, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

rx = float(proc.communicate()[0])

proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2" % intf, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

tx = float(proc.communicate()[0])

time.sleep(sleep)

proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $2}' | cut -d ':' -f 2" % intf, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

rx2 = float(proc.communicate()[0])

proc = subprocess.Popen("ifconfig %s | grep -v grep | grep bytes | awk '{print $6}' | cut -d ':' -f 2" % intf, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

tx2 = float(proc.communicate()[0])

rdiff = (rx2 - rx)/(1024.0 * sleep)
tdiff = (tx2 - tx)/(1024.0 * sleep)

print (rdiff, tdiff)
