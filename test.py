#!/usr/bin/python
#
#  This script takes input from a .csv file and creates new devices.
#  Any line in the .csv that begins with # is ignored
#
#  createde by Steve Meuse 9/25/2017  <smeuse@kentik.com>
#
import os
import stat
import json, requests, time
from os.path import expanduser
import os.path
import sys

filename = 'ad1.csv'


good = 0
bad = 0

#
<<<<<<< HEAD
#  This code was borrowed from Dan Rohan
=======
#  This code was borrowed from Da
>>>>>>> 2408848358f9f362eed2573b7fb71cd13ef46773
def get_creds():
    homeDir = expanduser("~")
    credsFile = ".kauth"
    credsFile = homeDir + "/" + credsFile
    perms = oct(stat.S_IMODE(os.lstat(credsFile).st_mode))
    if not perms == "0600":
            print "Your credentials file is not set to 600, please fix"
            sys.exit()
    if os.path.isfile(credsFile):
        with open(credsFile) as f:
            content = f.read()
            creds = json.loads(content)
            return(creds)
    else:
        pass

while get_creds() == False:
    break

def skip_comments(filename):
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip().startswith('#'):
               yield line



api = get_creds()['api']
email = get_creds()['email']
payload = {'Content-Type': 'application/json', 'X-CH-Auth-API-Token': api, 'X-CH-Auth-Email': email}

# Read in the json file for sites
with open('site.json', 'r') as data_file:
    json_data = data_file.read()
    data = json.loads(json_data)

mydict = {}
for f in data['sites']:
    mydict[f['site_name']] = f['id']

plandict = {'1k': '3620', '500': '3621'}

for line in skip_comments(filename):
    newline = line.rstrip()
<<<<<<< HEAD
=======
	# devicename,devicetype,devicedescription,planid,siteid,devicesamplerate,sendingips,devicesnmpip,devicesnmpcommunity = newline.split(",")
>>>>>>> 2408848358f9f362eed2573b7fb71cd13ef46773
    siteid,devicename,devicedescription,sendingips,v6add,asn,devicesnmpcommunity,devicesamplerate,planid = newline.split(",")
    iplist = [ sendingips ]
    site = siteid.upper()
    kentikjson = {}
    kentikjson['device_name']=devicename
    kentikjson['device_type']='router'
    kentikjson['device_description']=devicedescription
    kentikjson['plan_id']=int(plandict[planid])
    kentikjson['site_id']=mydict[site]
    kentikjson['device_sample_rate']=int(devicesamplerate)
    kentikjson['sending_ips']=iplist
    kentikjson['device_snmp_ip']=sendingips
    kentikjson['device_snmp_community']=devicesnmpcommunity
    kentikjson['device_bgp_type']='device'
    kentikjson['minimize_snmp']=False
    kentikjson['device_bgp_neighbor_ip']=sendingips
    kentikjson['device_bgp_neighbor_ip6']=v6add
    kentikjson['device_bgp_neighbor_asn']=asn
    kentikjson['device_bgp_password']=''

    device = {}
    device['device']=kentikjson
    kpush = json.dumps(device)
    print kpush

    rkentik = requests.post('https://api.kentik.com/api/v5/device', headers=payload, data=kpush)


    if rkentik.status_code == 201:
        print 'device "%s" added successfully' % (devicename)
        good += 1

    elif rkentik.status_code == 400:
        if 'Already Exists' in rkentik.text:
            print 'Device %s aleady exists in the Kentik device list' % (devicename)
        else:
            print 'Error code 400, your JSON is likely formatted incorrectly or you have a wrong data type for a json variable'
            bad += 1
            break

    elif rkentik.status_code == 401:
        print 'Error code 401, you are not authorized. Check your API Key or Kentik email address'
        bad += 1
        break

    else:
        print 'device "%s" not added: Error Code %s' % (devicename, rkentik.status_code)
        bad += 1

    time.sleep(1)

print "%s Devices sucessfully added \n%s devices failed to add" % (good, bad)
