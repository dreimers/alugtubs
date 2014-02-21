#this scripts periodically checks the activity on a machine (avg in/out bytes and avg load)
#when certain levels (see lin 17,18) are reached, the machine will shut down
import time
import subprocess as sub
startsleep = 15 # in minutes
sleeptime = 30 #in seconds
data_net = '/proc/net/dev'
data_load = '/proc/loadavg'
togglefile = '/var/log/autoshutdown/onoff'
interface = 'eth0'
bytes_start = 0
waitshutdown = '1' #how many minutes to wait before actual shutdown
n = 10 #how many entries have to be considered?

bytes_list = []
loads_list = []

#below that levels, we will shut down
bytes_level = 100
loads_level = 0.1

time.sleep(startsleep * 60)

def _get_bytes():
    f = open(data_net,'r')
    for line in f:
        if(interface in line):
            recv = int(line.split()[1])
	    sent = int(line.split()[9])
	    return recv + sent

def _get_load():
    f = open(data_load,'r')
    return float(f.readline().split()[1]) #load of last 5 min

def _get_off():
    f = open(togglefile,'r')
    i = int(f.readline())
    if i==1:
	return False #ON
    else:
	return True #OFF

def _call(cmd):
	p = sub.Popen(cmd,stdout=sub.PIPE,stderr=sub.PIPE,shell=True)
	(out, err) = p.communicate()
	if len(err)>0:
		print err 
		print "terminating"
		sys.exit(1)
	return out


while 1:
    if _get_off():
    	time.sleep(2*sleeptime)
	continue

    bytes_start = _get_bytes()
    time.sleep(sleeptime)

    bytes_per_cycle = _get_bytes() - bytes_start


    bytes_list.append(bytes_per_cycle)
    loads_list.append(_get_load())
    
    #wait until lists are full

    if ( len(bytes_list) < n or len(loads_list) < n ):
        continue
    #calc avereage of each list
    bytes_avg = sum(bytes_list[-n:]) / float(len(bytes_list))
    loads_avg = sum(loads_list[-n:]) / float(len(loads_list))
    print bytes_avg
    print loads_avg

    if(bytes_avg < bytes_level and loads_avg < loads_level):
	_call('shutdown -P +' + waitshutdown + ' "Abbrechen mit shutdown -c"')
	exit(0)
