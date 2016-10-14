import json

def getProductList(productFile):
    products = []
    for lineNumber, line in enumerate(productFile):
        try:
            products.append(json.loads(line))
        except ValueError:
            print("Incorrect JSON Formatting on line {}: '{}'".format(lineNumber, line))
            continue
    return products

def loadListings(listingFile, listingQueue, listingCount):
    for lineNumber, line in enumerate(listingFile):
        try:
            listingQueue.put((lineNumber + 1, json.loads(line)))
            listingCount.value += 1
        except ValueError:
            print("Incorrect JSON Formatting on line {}: '{}'".format(lineNumber, line))
            continue

def sortListingsByProduct(productQueue, products):
    sortedListings = {product["product_name"]: [] for product in products}
    
    while not productQueue.empty():
        listing, productIndex = productQueue.get()
        sortedListings[products[productIndex]["product_name"]].append(listing)
    return sortedListings

    
def printProductMatches(productQueue, products, outputFile):
    sortedListings = sortListingsByProduct(productQueue, products)

    for product_name in sortedListings:
        outputFile.write("{{\"product_name\": {}, \"listing\": [{}]}}\n".format(product_name, sortedListings[product_name]))
