from threading import Thread
import queue

continueOrganizingMatches = True

def organizeMatchesForPrinting(matchQueue, products, productMatches):
    global continueOrganizingMatches
    
    while continueOrganizingMatches:
        try:
            listing, productIndex = matchQueue.get_nowait()
            productMatches[products[productIndex]["product_name"]].append(listing)
            matchQueue.task_done()
        except queue.Empty:
            continue

#    return [{"product_name": product, "listing": sortedListings[product]} for product in sortedListings]    

def startMatchOrganizer(matchQueue, products, productMatches):    
    Thread(name="matchOrganizer", target=organizeMatchesForPrinting, args=(matchQueue, products, productMatches), daemon=True).start()
    
def monitorModel(listingQueue, stopProcesses, matchQueue, model):
    #There are four steps to knowing if the program is finished processing

    #1. Wait for the listing queue to empty, and for the processes to indicate 'task_done'
    listingQueue.join()

    #2. Stop the processes.
    stopProcesses(listingQueue)

    #3. Wait for the matchingQueue to be empty and have 'task_done'ed every listing. Next flag it to stop the loop
    matchQueue.join()
    continueOrganizingMatches = False

    #4. Toggle the flag so the GUI can see we are finished.
    model.currentlyProcessing = False

def flagIfProcessingFinished(listingQueue, stopProcesses, matchQueue, model):
    Thread(name="flagIfFinished", target=monitorModel, args=(listingQueue, stopProcesses, matchQueue, model)).start()
