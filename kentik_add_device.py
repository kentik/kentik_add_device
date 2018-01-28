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

# This is the file that contains the devices to be added
filename = 'sample.csv'

# Initialize the counters, see section on error checking
good = 0
bad = 0

#
#  This code was borrowed from Dan Rohan whith a few tweaks.
#  We're looking for $HOME/.kauth where the user creds should be stored
#  as a json object. We'll dump out if the file is world readable, forcing
#  the user to fix the perms.
#
#  Example:
#
#  {
#     "email":"email@useraccount.com",
#     "api":"87as76v76f87asd876g876asd876bh89asd"
#  }

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

#
#  Open up the .csv file and ignore any lines that begin with #
def skip_comments(filename):
    with open(filename, 'r') as f:
        for line in f:
            if not line.strip().startswith('#'):
               yield line


# Get the user credentials and get the http header put together for when we submit the API query
api = get_creds()['api']
email = get_creds()['email']
payload = {'Content-Type': 'application/json', 'X-CH-Auth-API-Token': api, 'X-CH-Auth-Email': email}


# OPTIONAL:  If you want to add the site by the text site name
# instead of the site_id, download the sites for the customer using
# the API tester and store the json in a text file. This nex section
# will read the file and load the contents into a dict.
# Read in the json file for sites
#
# with open('tata.json', 'r') as data_file:
#     json_data = data_file.read()
#     data = json.loads(json_data)
#
# sitesdict = {}
# for f in data['sites']:
#     mydict[f['site_name']] = f['id']
#

# This next section iterates over each line of the .csv file and assigns each csv into a variable.
# We then create the new Json object with the appropriate API variables. Kentikjson contains all the
# API variables.
#
#  Note: It's important to pay attention to the Json types for each variable. For example, 'device_name' is
#  a string, but iplist is an array of strings. Failure to assign the righ type rill result in a 400 error.
#  The API documentation lists all the types.
#
#  Another Note: If you are assigning a device to a site, the site must already exist. Future versions of this
#  script will likely dynamically create them, but it's currently a manual process

for line in skip_comments(filename):
	newline = line.rstrip()
    siteid,devicename,devicedescription,sendingips,v6add,asn,devicesnmpcommunity,devicesamplerate,planid = newline.split(",")
	iplist = [ sendingips ]
    #site = siteid.upper()  # Optional, if you use the sitedict and customer uses uppercase site names
	kentikjson = {}
	kentikjson['device_name']=devicename
	kentikjson['device_type']='router'
	kentikjson['device_description']=devicedescription
	kentikjson['plan_id']=int(planid)
	kentikjson['site_id']=int)siteid) # or sitesdict[siteid]
	kentikjson['device_sample_rate']=int(devicesamplerate)
	kentikjson['sending_ips']=iplist
	kentikjson['device_snmp_ip']=devicesnmpip
	kentikjson['device_snmp_community']=devicesnmpcommunity
    kentikjson['device_bgp_neighbor_ip']=sendingips
    kentikjson['device_bgp_neighbor_ip6']=v6v6add
    kentikjson['device_bgp_neighbor_asn']=asn
    kentikjson['device_bgp_password']=''
	kentikjson['device_bgp_type']='device'
	kentikjson['minimize_snmp']=False


#
#  Once Kentikjson is populated, we need to put that list of json variables into a new json object called "device"
#
#  INSERT example of a valid object
	device = {}
	device['device']=kentikjson
	kpush = json.dumps(device)
	#print kpush
	rkentik = requests.post('https://api.kentik.com/api/v5/device', headers=payload, data=kpush)


# The rest is basically looking at the output of each request post and looking for error messages.
# I've tried to figure out some basic issues with trial and Error. If a device isn't successfully
# added I increase the bad counter. This allows for a basic report at the end of the script to
# let you know how many sucess/fails you had.
#
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
