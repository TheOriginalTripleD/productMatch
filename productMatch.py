#!/usr/bin/python3

import argparse
import sys
import model, view

parser = argparse.ArgumentParser(description = "Match a JSON file of product listings to a JSON file of products", prog='productMatch')

parser.add_argument('output', type=argparse.FileType("w"), help='output file')
parser.add_argument('-l', metavar="Listings", default='data/listings.txt', type=open,
                    help='File containing the product listings (default "data/listings.txt")')
parser.add_argument('-p', metavar="Products", default='data/products.txt', type=open,
                    help='File containing the products (default "data/products.txt")')
parser.add_argument('-t', metavar="Processors", type=int, default=2,
                    help='Number of processors to use (default 2)')

try:
    arguments = parser.parse_args()
except FileNotFoundError:
    sys.exit(FileNotFoundError)

if arguments.t <= 0:
    sys.exit("productMatch: error: Processor count must be greater than or equal to 1")

model = model.Model(arguments.t, arguments.p, arguments.l, arguments.output)

view = view.View(model)

view.start()
