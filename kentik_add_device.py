#!/usr/bin/python
#
#  This script takes input from a .csv file and creates new devices. 
#  Any line in the .csv that begins with # is ignored
#
#  createde by Steve Meuse 9/25/2017  <smeuse@kentik.com>
#

import json, requests, time

filename = 'sample.csv'

payload = {'Content-Type': 'application/json', 'X-CH-Auth-API-Token': 'your-api-token', 'X-CH-Auth-Email': 'your@email.com'}

good = 0 
bad = 0

def skip_comments(filename):
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip().startswith('#'):
               yield line
               
for line in skip_comments(filename):
	newline = line.rstrip()
	devicename,devicetype,devicedescription,planid,siteid,devicesamplerate,sendingips,devicesnmpip,devicesnmpcommunity = newline.split(",")
	intrate = int(devicesamplerate)
	intplan = int(planid)
	intsite = int(siteid)
	iplist = [ sendingips ]
	kentikjson = {}
	kentikjson['device_name']=devicename
	kentikjson['device_type']=devicetype
	kentikjson['device_description']=devicedescription
	kentikjson['plan_id']=intplan
	kentikjson['site_id']=intsite
	kentikjson['device_sample_rate']=intrate
	kentikjson['sending_ips']=iplist
	kentikjson['device_snmp_ip']=devicesnmpip
	kentikjson['device_snmp_community']=devicesnmpcommunity
	kentikjson['device_bgp_type']='none'
	kentikjson['minimize_snmp']=False

	device = {}
	device['device']=kentikjson
	kpush = json.dumps(device)
#	print kpush
	rkentik = requests.post('https://api.kentik.com/api/v5/device', headers=payload, data=kpush)

	
	if rkentik.status_code == 201:
		print 'device "%s" added successfully' % (devicename)
		good += 1
	
	elif rkentik.status_code == 400:
		if 'Already Exists' in rkentik.text:
			print 'Device %s already exists in the Kentik device list' % (devicename)
		else:
			print 'Error code 400, your JSON is likely formatted incorrectly or you have a wrong data type for a json variable'
			break
	
	elif rkentik.status_code == 401:
		print 'Error code 401, you are not authorized. Check your API Key or Kentik email address'
		break
	
	else:
		print 'device "%s" not added: Error Code %s' % (devicename, rkentik.status_code)
		bad += 1
	
	time.sleep(1)
	
print "%s Devices sucessfully added \n%s devices failed to add" % (good, bad)
