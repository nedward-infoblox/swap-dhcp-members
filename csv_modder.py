import csv
import requests
import urllib3
from sys import argv, exit
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def outex(st):
	with open('output.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerows(st)
	csvfile.close()

def prix(str):
	print(str)
	exit()

def modify_csv(networks_csv, ranges_csv, foa_csv, arg1, arg2):
	# Initialize output variable as an empty list
	global i
	
	output = []
	nw = []

	# Open networks.csv and read it into a list of rows
	with open(networks_csv, 'r') as f:
		reader = csv.reader(f)
		rows = list(reader)

	# Find index of dhcp_members
	i = rows[0].index("dhcp_members")
	output.extend([rows[0]])

	# Filter network rows containing old server in members list and store them in output
	output.extend([row for row in rows if arg1 in row[i].split(',')])

	networks = []
	# Append new servers to the existing values in the "dhcp_members" column
	for row in output[1:]:
		networks.append(row[1])
		for ar in arg2.split(","):
			if ar not in row[i]:
				row[i] = row[i] + ',' + ar

	# Find the new FOA
	# Open foa.csv and read it into a list of rows
	with open(foa_csv, 'r') as f:
		reader = csv.reader(f)
		foa = list(reader)

	# Find new foa of the given servers
	failoverAssociation = ''.join([l[0] for l in foa if l[2] in arg2.split(',') and l[3] in arg2.split(',')])

	# Open ranges.csv and read it into a list of rows
	with open(ranges_csv, 'r') as f:
		reader = csv.reader(f)
		lines = list(reader)

	server_address = '172.20.24.61'
	gm_user = 'M554644'
	gm_pwd = 'Welcome@123'

	startIP = []
	for n in networks:
		url1='https://{}/wapi/v2.9/range?network={}'.format(server_address,n)
		response1 = requests.get(url1, verify=False, auth=(gm_user, gm_pwd)).json()
		if len(response1) != 0:
			startIP.append(response1[0]['start_addr'])

	# Find indices
	j = lines[0].index("failover_association")
	s = lines[0].index("start_address*")
	m = lines[0].index("member")

	output.extend([lines[0]])
	for r in lines[1:]:
		try:
			# Check if start_address is present in list of start IPs, if yes replace foa with new foa
			if r[s] in startIP:
				newr = list(map(lambda x: x.replace(r[j], failoverAssociation), r))
				newr = list(map(lambda x: x.replace(newr[m], arg1), newr))
				if newr[0] == "dhcprange":
					output.append(newr)
		except Exception as e:
			print("Error: ", e)

	return output

# Calling function
result1 = modify_csv('networks.csv', 'ranges.csv', 'foa.csv', argv[1], argv[2])
result2 = modify_csv('networks.csv', 'ranges.csv', 'foa.csv', argv[1], argv[2])

for entry in result1[1:]:
	if entry[0] == "network":
		entry[i] = entry[i].replace(argv[1], '').replace(',,', ',').strip(',')
		result2.append(entry)

outex(result2)
