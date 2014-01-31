#!/usr/bin/env python

import sys
import csv
import argparse

parser = argparse.ArgumentParser()


parser.add_argument('infile', nargs='?', type=argparse.FileType('rb'),
                    default=sys.stdin, help="Greater Giving Item Export CSV (ITM-10, selected to be Online Auction Types only. Default is STDIN")

parser.add_argument('outfile', nargs='?', type=argparse.FileType('wb'),
                    default=sys.stdout,   help="Bidding For Good Import CSV. Default is STDOUT")

args = parser.parse_args()

def convert_gg_to_b4g(gg_dict):
    b4g_dict={}
    b4g_dict['Item Name'] = gg_dict['Item Name']
    return b4g_dict

gg_rows = []
input_file = csv.DictReader(args.infile)
for row in input_file:
    gg_rows.append(row)

b4g_rows = map(convert_gg_to_b4g, gg_rows)

output_file = csv.DictWriter(args.outfile, ['Item Name'], extrasaction='ignore', )
for row in b4g_rows:
    output_file.writerow(row)
    
