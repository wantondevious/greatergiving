#!/usr/bin/env python

import sys
import csv
import argparse
import re

parser = argparse.ArgumentParser()


parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'),
                    default=sys.stdin, help="Greater Giving Item Export CSV (ITM-10, selected to be Online Auction Types only. Default is STDIN")

parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'),
                    default=sys.stdout,   help="Bidding For Good Import CSV. Default is STDOUT")

args = parser.parse_args()

b4g_header=['Lot Number', 'Quantity', 'Item Name', 'Item Description', 'Special Note', 'Donor Name', 'Donor URL', 'Donor Logo', 'Category', 'Item Type', 'Item Attributes', 'Item Location', 'Featured Item', 'Bidder Community', 'Cost', 'Estimated Value', 'Value Display', 'Online Bidding', 'Opening Bid', 'Reserve Price', 'Bid Increment', 'Buy Now Price', 'Online Open Date', 'Online Open Time', 'Online Close Date', 'Online Close Time', 'Status', 'Live Event', 'Item Image']

def clean(string):
    if string is not None:
        #string = re.sub('[^0-9A-Za-z!,\.:\/]', ' ', string)
        string = re.sub('[\r\n]', ' ', string)
        string = re.sub('[ ]{2,}', ' ', string)
    return string 


def convert_gg_to_b4g(gg_dict):
    b4g_dict={}
    b4g_dict['Lot Number'] = gg_dict['Item Number']
    b4g_dict['Item Name'] = gg_dict['Item Name']
    b4g_dict['Item Description'] = clean(gg_dict['Description'])
    b4g_dict['Donor Name'] = gg_dict['Donors']
    b4g_dict['Item Location'] = gg_dict['Location']
    b4g_dict['Cost'] = gg_dict['Cost']
    b4g_dict['Estimated Value'] = gg_dict['Value']
    b4g_dict['Category'] = gg_dict['Category Name']
    return b4g_dict

gg_rows = []
input_file = csv.DictReader(args.infile)
for row in input_file:
    gg_rows.append(row)

sys.stderr.write("%d rows read from input.\n" % len(gg_rows))

b4g_rows = map(convert_gg_to_b4g, gg_rows)

output_file = csv.DictWriter(args.outfile, b4g_header, extrasaction='ignore')
for row in b4g_rows:
    output_file.writerow(row)
    
