import json, queue, multiprocessing

def getProductList(productFile):
    products = []

    for lineNumber, line in enumerate(productFile):
        try:
            products.append(json.loads(line))
        except ValueError:
            print("Incorrect JSON Formatting on line {}: '{}'".format(lineNumber, line))
            continue
    return products

def getListings(listingFileHandle):
    listingQueue = multiprocessing.JoinableQueue()
    totalListings = 0
    
    for lineNumber, line in enumerate(listingFileHandle):
        try:
            listingQueue.put(json.loads(line))
            totalListings += 1
        except ValueError:
            print("Incorrect JSON Formatting on line {}: '{}'".format(lineNumber, line))
            continue
        
    return listingQueue, totalListings

def sortListingsByProduct(matchQueue, products):
    sortedListings = {product["product_name"]: [] for product in products}
    
    while True:
        try:
            listing, productIndex = matchQueue.get_nowait()
            sortedListings[products[productIndex]["product_name"]].append(listing)
        except queue.Empty:
            break

    return [{"product_name": product, "listing": sortedListings[product]} for product in sortedListings]

def printProductMatches(productMatches, outputFile):
    for productMatch in [{"product_name": product, "listing":productMatches[product]} for product in productMatches]:
        outputFile.write(json.dumps(productMatch) + "\n")
