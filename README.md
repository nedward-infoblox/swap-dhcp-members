# mylan-change-members
Script to create an Infoblox CSV Import file to move all networks and ranges belonging to one Member to another Member+FOA

1. Download the CSV of all Networks - networks.csv
2. Download the CSV of all Ranges - ranges.csv
3. Download the CSV of all FoA - foa.csv
4. Add a column titled 'EA-parent_network' to the ranges.csv file

Steps:
1. Run range_update_parent.py to update the Ranges with their corresponding Network addresses 
2. Run csv_modder.py. Syntax:

Usage:
```
python3 csv_creator.py [-h] [-s SOURCE] [-m MEMBER] [-f FOA] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        Hostname of server from which DHCP data must be moved
  -m MEMBER, --member MEMBER
                        Hostname of server to which DHCP data must be moved
  -f FOA, --foa FOA     Name of Failover Association to which DHCP data must be moved
  -o OUTPUT, --output OUTPUT
                        Output filename
```
