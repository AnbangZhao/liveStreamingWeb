#!/usr/bin/env python

import sys
import subprocess
import time

# usage python calBandwidth ip port dir
# e.g. python calBandwidth 10.0.0.1 1259 src
runtimeint = 5
runtime = str(runtimeint) + 's'
filename = "tcpdumpSample"

def illegalArgs():
    if len(sys.argv) != 4:
        print "usage: python calBandwidth ip port dir"
        return True
    return False

def main():
    if(illegalArgs()):
        return
    ip = sys.argv[1]
    port = sys.argv[2]
    direction = sys.argv[3]
    subprocess.Popen(['rm', '-rf', filename], shell = False)
    subprocess.call('sudo timeout ' + runtime + ' tcpdump -i eth0 -n ' + direction +' ' + ip + ' and port ' + port + ' > ' + filename, shell = True)
    print "finished"
    calculate(direction)

def calculate(direction):
    #time.sleep(runtimeint + 1)
    dumpFile = open(filename, "r")
    count = 0
    seqDict = {}
    distinct = 0
    allCounts = 0
    for line in dumpFile:
        words = line.split()
        if len(words) != 21:
            continue
        count += int(words[len(words) - 1])
        ip = ''
        if direction == 'src':
            targetip = words[4]
        else:
            targetip = words[2]
        seq = words[8]
        whole = targetip+seq
        if seqDict.get(whole) == None:
            seqDict[whole] = 1
            distinct += 1
        allCounts += 1

    count = count * 8/1024
    if allCounts == 0:
        allCounts = 1
    lossRate = float(allCounts - distinct)/allCounts
    bandwidth = float(count)/float(runtimeint)
    print 'total count is', count, 'kb'
    print 'average bandwidth is', bandwidth, 'kbs'
    print 'loss rate is', lossRate

if __name__ == "__main__":
    main()
