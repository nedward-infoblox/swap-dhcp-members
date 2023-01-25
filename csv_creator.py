import csv
import argparse
# import urllib3
from sys import exit
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize parser
parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-s", "--source", help = "Hostname of server from which DHCP data must be moved")
parser.add_argument("-m", "--member", help = "Hostname of server to which DHCP data must be moved")
parser.add_argument("-f", "--foa", help = "Name of Failover Association to which DHCP data must be moved")
parser.add_argument("-o", "--output", help = "Output filename (Default: output.csv)", default='output.csv')
 
# Read arguments from command line
args = parser.parse_args()


def outex(st):
	with open(args.output, 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile)
		spamwriter.writerows(st)
	csvfile.close()

def prix(str):
	print(str)
	exit()

# prix(args.source)



def modify_csv(networks_csv, ranges_csv):
	# Initialize output variable as an empty list
	global i
	
	output = []
	networks = []
	servers = []

	# Check if moving to FOA. If yes, find corresponding servers
	if args.foa:
		with open("foa.csv", 'r') as f:
			reader = csv.reader(f)
			foa = list(reader)

        # Find new foa of the given servers
		foa_servers = [[l[2],l[3]] for l in foa if l[0] == args.foa]
		servers = foa_servers[0]
	if args.member:
		a = args.member
		servers.extend(a.split(','))


	# Open networks.csv and read it into a list of rows
	with open(networks_csv, 'r') as f:
		reader = csv.reader(f)
		rows = list(reader)

	# Find index of dhcp_members
	i = rows[0].index("dhcp_members")
	output.extend([rows[0]])

	# Filter network rows containing old server in members list and store them in output
	output.extend([row for row in rows if args.source in row[i].split(',')])

	# Append new servers to the existing values in the "dhcp_members" column
	for row in output[1:]:
		networks.append(row[1])
		for ar in servers:
			if ar not in row[i]:
				row[i] = row[i] + ',' + ar
	
   
	# Open ranges.csv and read it into a list of rows
	with open(ranges_csv, 'r') as f:
		reader = csv.reader(f)
		lines = list(reader)

	# Find indices
	j = lines[0].index("failover_association")
	s = lines[0].index("EA-parent_network")
	m = lines[0].index("member")
	sa = lines[0].index("server_association_type")

	lines[0][s] = ''
	output.extend([lines[0]])
	
	for r in lines[1:]:
		try:
			if r[0] == 'dhcprange' and r[s] in networks:
				if args.foa:
					r[j] = args.foa
					r[m] = ''
					r[sa] = 'FAILOVER'
				elif args.member:
					r[m] = a.split(',')[0]
					r[j] = ''
					r[sa] = 'MEMBER'	
				r[s] = ''
				output.append(r)
		except Exception as e:
			print("Error: ", e)
	# print(output)
	return output

# Calling function
result1 = modify_csv('networks.csv', 'ranges_updated.csv')
result2 = modify_csv('networks.csv', 'ranges_updated.csv')

# prix(result1)
for entry in result1[1:]:
	if entry[0] == "network":
		entry[i] = entry[i].replace(args.source, '').replace(',,', ',').strip(',')
		result2.append(entry)

outex(result2)
