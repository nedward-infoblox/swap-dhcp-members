import csv
import ipaddress
import tqdm
from sys import argv, exit

def prix(*str):
    print(str)
    exit()

def outex(st):
    with open('ranges_updated.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(st)
    csvfile.close()
    exit()

output = []

with open('networks.csv', 'r') as f:
    reader = csv.reader(f)
    network_lines = list(reader)

networks = [netmask[1]+'/'+str(ipaddress.IPv4Network('0.0.0.0/'+netmask[2]).prefixlen) for netmask in network_lines[1:]]

with open('ranges.csv', 'r') as f:
    reader = csv.reader(f)
    ranges = list(reader)

ranges[0].append("EA-parent_network")

s1 = ranges[0].index("start_address*")
s2 = ranges[0].index("end_address*")
p = ranges[0].index("EA-parent_network")

# prix(len(ranges[0]),p,ranges[0][p])
output.extend([ranges[0]])

# for n in networks:
#     for r in ranges[2:]:
#         if ipaddress.ip_address(r[s1]) in ipaddress.ip_network(n) and ipaddress.ip_address(r[s2]) in ipaddress.ip_network(n):
#             r.append(n)
#             output.append(r)
#             # print(r[s1], r[s2], r[p]+'               ', end='\r')

for r in tqdm.tqdm(ranges):
    if r[0] == 'dhcprange':
        for n in networks:
            if ipaddress.ip_address(r[s1]) in ipaddress.ip_network(n) and ipaddress.ip_address(r[s2]) in ipaddress.ip_network(n):
                # print(n)
                r.append(n.split('/')[0])
                output.append(r)
                break

outex(output)
# output.extend([ranges[0]])
# for r in ranges[2:]:
#     url1='https://{}/wapi/v2.9/range?start_addr={}'.format(server_address,r[s])
#     response1 = requests.get(url1, verify=False, auth=(gm_user, gm_pwd)).json()
#     if len(response1) != 0:
#         r[p] = response1[0]['network'].split('/')[0]
#         output.append(r)
#     print(r[s]+'    '+r[p]+'        ', end='\r')
# outex(output)