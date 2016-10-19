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
parser.add_argument('-t', metavar="Threads", type=int, default=2,
                    help='Number of processors to use (default 2)')
parser.add_argument("-a", metavar="Accuracy", default=2, type=int,
                    help="Level of accuracy for matching. Can be 0, 1, or 2. 0 has the loosest  " +
                    "criteria for matching, 2 has the most strict. (default 2)")

try:
    arguments = parser.parse_args()
except FileNotFoundError:
    sys.exit(FileNotFoundError)

if arguments.t <= 0:
    sys.exit("productMatch: error: Processor count must be greater than or equal to 1")

model = model.Model(arguments.t, arguments.p, arguments.l, arguments.output, arguments.a)

view = view.View(model)

view.start()


'''
products = files.getProductList(arguments.p)

print("Spawning Processes")

listingQueue, matchQueue, listingTotal = processes.createProcessPool(arguments.t, products, arguments.a)

print("Loading Listings")

files.loadListings(arguments.l, listingQueue, listingTotal)

processes.waitForProcessesToFinish(listingQueue)
processes.stopProcesses()

#print("Empty") if matchQueue.empty() else print("has something")

print("Writing File")

files.printProductMatches(matchQueue, products, arguments.output)

print("Finished")
'''
