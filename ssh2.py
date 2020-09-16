#!/bin/python

import json
import os
import sys
import re
import fnmatch
import subprocess

user = "cloud-user"
aliases = []
Names_Found = []

cloud = raw_input("Select your cloud"
    "\n1) AWS"
    "\n2) Google"
    "\n\n# ")

env = raw_input ("Which envrionment?"
    "\n1) Production"
    "\n2) Staging"
    "\n3) Development"
    "\n4) Sandbox"
    "\n5) Tools"
    "\n\n# ")

if (cloud == "1" and env == "1"):
    print "Setting config for GDP"
    config = '/home/larwal/.scalr/GDP.yaml'
elif (cloud == "1" and env == "2"):
    print "Setting config for GDS"
    config = '/home/larwal/.scalr/GDS.yaml'
elif (cloud == "1" and env == "3"):
    print "Setting config for GDD.yaml"
    config = '/home/larwal/.scalr/GDD.yaml'
elif (cloud == "1" and env == "4"):
    print "Setting config for GDSB"
    config = '/home/larwal/.scalr/GDSB.yaml'
elif (cloud == "1" and env == "5"):
    print "Setting config for GDT"
    config = '/home/larwal/.scalr/GDT.yaml'
elif (cloud == "2" and env == "1"):
    print "Setting config for PP"
    config = '/home/larwal/.scalr/PP.yaml'
elif (cloud == "2" and env == "2"):
    print "Setting config for PS"
    config = '/home/larwal/.scalr/PS.yaml'
elif (cloud == "2" and env == "3"):
    print "Setting config for PD"
    config = '/home/larwal/.scalr/PD.yaml'
elif (cloud == "2" and env == "4"):
    print "Google does not have a sandbox"
    sys.exit()
elif (cloud == "2" and env == "5"):
    print "Setting config for PT"
    config = '/home/larwal/.scalr/PT.yaml'

FarmName = raw_input("What is part of the farm name? ")

os.system("scalr-ctl --config %s farms list > farmlist.json" %(config))

with open('farmlist.json', 'r') as f:
    item_dict = json.load(f)
    farmCount = len(item_dict['data'])
    realfarmcount = farmCount - 1
    f.closed

fcount = 0

while realfarmcount >= fcount:
    with open('farmlist.json', 'r') as f:
        json_dict = json.load(f)
        farmname=str(json_dict['data'][fcount]['name'])
        f.closed

    if FarmName not in farmname:
        fcount += 1
        pass
    else:
        Names_Found.append('%s' %(farmname))
        fcount += 1

print "\nThe following farms were found:\n"

ncount = 1

for name in Names_Found:
    print ("%s) %s" %(ncount, name))
    ncount += 1

sresponse = raw_input("\nIs your farm in the list (Y,N)? ")

if sresponse in ('Y', 'y'):
    nresponse = raw_input("\nSelect the number for your farm: ")
    ncount = int(nresponse)
    ncount -= 1
    nfarm = Names_Found[ncount]

    fcount = 0
    while realfarmcount >= fcount:
        with open('farmlist.json', 'r') as f:
            json_dict = json.load(f)
            farmname=str(json_dict['data'][fcount]['name'])
            f.closed

        #if nfarm not in farmname:
	if nfarm != farmname:
            fcount += 1
            pass
        else:
            with open('farmlist.json', 'r') as f:
                j = json.load(f)
                farmId =j['data'][fcount]['id']
                f.closed
                break

    os.system("scalr-ctl --config %s farm-roles list --farmId %s > farminfo.json" %(config, farmId))

    with open('farminfo.json', 'r') as f:
        item_dict = json.load(f)
        dataCount = len(item_dict['data'])
        realcount = dataCount - 1
        f.closed

    count = 0

    while realcount >= count:
        with open('farminfo.json', 'r') as f:
            j = json.load(f)
            role_alias = j['data'][count]['alias']
            aliases.append('%s' %(role_alias))
            f.closed
        count += 1

    print "\n"
    scount = 1
    for server in aliases:
        print ("%s) %s" %(scount, server))
        scount += 1


    sresponse = raw_input("\nWhich role do you want to log into? ")

    datacount = int(sresponse)

    datacount -= 1

    rolealias = aliases[datacount]

    with open ('farminfo.json', 'r') as f:
        j = json.load(f)
        roleID =j['data'][datacount]['id']
        f.closed

    os.system("scalr-ctl --config %s farm-roles list-servers --farmRoleId %s > roleinfo.json" %(config, roleID))

    with open('roleinfo.json','r') as f:
        j = json.load(f)
        IP = j['data'][0]['privateIp'][0]
        f.closed

    for file in os.listdir("/home/larwal/cloud-wp/keys/"):
        if fnmatch.fnmatch(file, '*%s*' %(farmId)):
            key = ("/home/larwal/cloud-wp/keys/%s" %(file))

    print ("\nLogging into %s as user %s\n" %(rolealias, user))

    userhost = ("%s@%s" % (user, IP))

    os.system("ssh -i %s %s" %(key, userhost))

    print "\nThanks for logging in!"

elif sresponse in ('N', 'n'):

    farmId = raw_input("\nWhat is the FarmID? ")

    os.system("scalr-ctl --config %s farm-roles list --farmId %s > farminfo.json" %(config, farmId))

    with open('farminfo.json', 'r') as f:
        item_dict = json.load(f)
        dataCount = len(item_dict['data'])
        realcount = dataCount - 1
        f.closed

    count = 0
    while realcount >= count:
        with open('farminfo.json', 'r') as f:
            j = json.load(f)
            role_alias = j['data'][count]['alias']
            aliases.append('%s' %(role_alias))
            f.closed
        count += 1

    print "\nWhich role do you want to log into?"

    lcount = 1

    for role in aliases:
        print ("%s) %s" %(lcount, role))
        lcount += 1

    response2 = raw_input("Enter response: ")
    lcount -= 1

    datacount = int(response2)

    datacount  -= 1

    rolealias = aliases[datacount]

    count = 0
    while realcount >= count:
        with open('farminfo.json', 'r') as f:
            json_dict = json.load(f)
            alias=str(json_dict['data'][count]['alias'])
            f.closed

        if rolealias not in alias:
            count += 1
            pass
        else:
            with open('farminfo.json', 'r') as f:
                j = json.load(f)
                roleID =j['data'][count]['id']
                f.closed
            count += 1

    os.system("scalr-ctl --config %s farm-roles list-servers --farmRoleId %s > roleinfo.json" %(config, roleID))

    with open('roleinfo.json','r') as f:
        j = json.load(f)
        IP = j['data'][0]['privateIp'][0]
        f.closed


    for file in os.listdir("/home/larwal/cloud-wp/keys/"):
        if fnmatch.fnmatch(file, '*%s*' %(farmId)):
            key = ("/home/larwal/cloud-wp/keys/%s" %(file))

    print ("\nLogging into %s as user %s" %(rolealias, user))

    userhost = ("%s@%s" % (user, IP))

    os.system("ssh -i %s %s" %(key, userhost))

    print "\nThanks for logging in!"

else:
    print "Invalid response. Exiting script"
    os.remove('farmlist.json')
    os.remove('farminfo.json')
    os.remove('roleinfo.json')
    sys.exit(1)

os.remove('farmlist.json')
os.remove('farminfo.json')
os.remove('roleinfo.json')
