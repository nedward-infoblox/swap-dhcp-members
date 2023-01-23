import csv
import requests
import urllib3
from sys import argv, exit
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def prix(str):
    print(str)
    exit()
def outex(st):
    with open('output.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        spamwriter.writerows(st)
    csvfile.close()
    exit()
output = []
with open('ranges.csv', 'r') as f:
    reader = csv.reader(f)
    ranges = list(reader)

server_address = '172.20.24.61'
gm_user = 'M554644'
gm_pwd = 'Welcome@123'

s = ranges[0].index("start_address*")
p = ranges[0].index("EA-parent_network")

output.extend([ranges[0]])
for r in ranges[2:]:
    url1='https://{}/wapi/v2.9/range?start_addr={}'.format(server_address,r[s])
    response1 = requests.get(url1, verify=False, auth=(gm_user, gm_pwd)).json()
    if len(response1) != 0:
        r[p] = response1[0]['network'].split('/')[0]
        output.append(r)
    print(r[s]+'    '+r[p]+'        ', end='\r')
outex(output)