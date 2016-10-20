from multiprocessing import Queue, JoinableQueue, Value, Process

processes = []

def matchListingsToProducts(productMatcher, listingQueue, matchQueue, listingsProcessed, matches, ambiguous):
    
    while True:
        listing = listingQueue.get()

        if listing is None:
            listingQueue.task_done()
            break

        matchingProductIndex = productMatcher.findMatchingProduct(listing)
        
        # -2 = no match, -1 = ambiguous 
        if matchingProductIndex >= 0:
            matches.value += 1
            matchQueue.put((listing, matchingProductIndex))
        elif matchingProductIndex == -1:
            ambiguous.value += 1

        listingsProcessed.value += 1
        listingQueue.task_done()

def stopProcesses(listingQueue):
    global processes
    
    for process in processes:
        listingQueue.put(None)
        
    listingQueue.join()
    
    for process in processes:
        process.join()
        
def createProcesses(processCount, masterMatchingObject, listingQueue, matchQueue, listingsProcessed, matches, ambiguous):
    
    for count in range(0, processCount):
        processes.append(Process(name="process-{}".format(count),daemon=True, target=matchListingsToProducts, args=(masterMatchingObject.copy(), listingQueue, matchQueue, listingsProcessed, matches, ambiguous)))
        
        processes[-1].start()
