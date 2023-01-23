# mylan-change-members
Script to create an Infoblox CSV Import file to move all networks and ranges belonging to one Member to another Member+FOA

1. Download the CSV of all Networks - networks.csv
2. Download the CSV of all Ranges - ranges.csv
3. Download the CSV of all FoA - foa.csv
4. Add a column titled 'EA-parent_network' to the ranges.csv file

Steps:
1. Run range_update_parent.py to update the Ranges with their corresponding Network addresses 
2. Run csv_modder.py. Syntax:

python3 csv_modder.py <current server name> <new server name 1>,<new server name 2> <output filename>
