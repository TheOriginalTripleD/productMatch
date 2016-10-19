from multiprocessing import Queue, JoinableQueue, Value, Process

processes = []

def matchListingsToProducts(productMatcher, listingQueue, matchQueue, listingsProcessed):
    
    while True:
        listing = listingQueue.get()

        if listing is None:
            listingQueue.task_done()
            break

#        print("processing {}".format(listingNumber), end="\r")
#        print("Processing {} of {}".format(listingNumber, listingTotal.value), end="\r")

        matchingProductIndex = productMatcher.findMatchingProduct(listing)
        
        # Returns -1 if no match is found
        if matchingProductIndex >= 0:
            matchQueue.put((listing, matchingProductIndex))

        listingsProcessed.value += 1
        listingQueue.task_done()

    return

def stopProcesses(listingQueue):
    global processes
    
    for process in processes:
        listingQueue.put(None)
        
    listingQueue.join()
    
    for process in processes:
        process.join()
        
def createProcesses(processCount, masterMatchingObject, listingQueue, matchQueue, listingsProcessed):
    
    for count in range(0, processCount):
        processes.append(Process(name="process-{}".format(count),daemon=True, target=matchListingsToProducts, args=(masterMatchingObject.copy(), listingQueue, matchQueue, listingsProcessed)))
        
        processes[-1].start()
