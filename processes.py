import matching
from multiprocessing import Queue, JoinableQueue, Value, Process

listings = JoinableQueue()
productMatches = Queue()

processes = []

listingCount = Value('i', 0)

def matchListingsToProducts(productMatcher, listingCount):
    
    while True:
        listingNumber, listing = listings.get()
        print("Processing {} of {}".format(listingNumber, listingCount.value), end="\r")
        
        pmatchingProductIndex = productMatcher.findMatchingProduct(listing)
        # Returns -1 if no match is found
        if matchingProductIndex > 0:
            productMatches.put((listing, matchingProductIndex))
            
        listings.task_done()

def waitForProcessesToFinish():
    global listings

    listings.join()
    print("")
        
def stopProcesses():
    global listingCount
    
    for process in processes:
        process.terminate()
        
def createProcessPool(processCount, products, productToListingMap, requiredFields, desiredFields, accuracy):
    global processes, listingCount
    
    for count in range(0, processCount):
        productMatcher = matching.Matching(products, productToListingMap, requiredFields, desiredFields, accuracy)

        processes.append(Process(name="process-{}".format(count),daemon=True, target=matchListingsToProducts, args=(productMatcher,listingCount)))
        
        processes[-1].start()

