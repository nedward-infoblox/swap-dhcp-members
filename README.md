# Swap DHCP Member
Script to create an Infoblox CSV Import file to move all networks and ranges belonging to a Member to other Member(s) or Failover Association, without the use of API

## Prerequisites
1. Download the CSV of all Networks (Infoblox format) - **networks.csv**
2. Download the CSV of all Ranges (Infoblox format) - **ranges.csv**
3. Download the CSV of all FoA - **foa.csv**

## Steps:
1. Run `range_update_parent.py` to update the ranges.csv file with Network addresses under 'EA-parent_network' header and rewrite to **ranges_updated.csv** file
2. Run `csv_creator.py`
3. Import the output file into Infoblox with **Override** as the Import option

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

