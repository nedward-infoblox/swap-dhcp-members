# mylan-change-members
Script to create an Infoblox CSV Import file to move all networks and ranges belonging to one Member to other Member(s) or Failover Association

1. Download the CSV of all Networks - networks.csv
2. Download the CSV of all Ranges - ranges.csv
3. Download the CSV of all FoA - foa.csv
4. Add a column titled 'EA-parent_network' to the ranges.csv file

## Steps:
1. Run range_update_parent.py to update the Ranges with their corresponding Network addresses 
2. Run csv_creator.py

## Usage:
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
                        Output filename (Default: output.csv)
```

## Examples:

### Move Networks from one server to a list of other Members
- Assigns the first listed Member as server for Ranges
```
python3 csv_creator.py -s old_server.infoblox.local -m new_1.infoblox.local,new_2.infoblox.local,new_3.infoblox.local
```

### Move Networks from one server to a Failover Association
- Finds the Members associated with the FoA and assigns them to the Network
```
python3 csv_creator.py -s old_server.infoblox.local -f APAC_FOA
```

### Do both of the above and write to 'import-data.csv' file
- Finds the Members associated with the FoA and assigns them to the Network along with the listed Members
- Ranges are assigned to the FoA
```
python3 csv_creator.py -s old_server.infoblox.local -m new_1.infoblox.local,new_2.infoblox.local -f APAC_FOA -o import-data.csv
```

