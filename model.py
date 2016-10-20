import threads, processes, multiprocessing, matching, files

class Model():
    def __init__(self, processCount, productFileHandle, listingFileHandle, outputFileHandle):
        #Flag to indicate if proccessing is ongoing
        self.currentlyProcessing = False

        self.processCount = processCount
        self.products = files.getProductList(productFileHandle)
        
        self.listingQueue, self.totalListings = files.getListings(listingFileHandle)
        self.listingsProcessed = multiprocessing.Value("i", 0)

        self.matchQueue = multiprocessing.JoinableQueue()
        self.productMatches = {product["product_name"]: [] for product in self.products}
        
        self.outputFileHandle = outputFileHandle
        self.masterMatchingObject = matching.Matching(self.products)

        self.matches = multiprocessing.Value("i", 0)
        self.ambiguous = multiprocessing.Value("i", 0)
        
    def startLookingForMatches(self):
        self.currentlyProcessing = True
             
        threads.startMatchOrganizer(self.matchQueue, self.products, self.productMatches)
        
        processes.createProcesses(self.processCount, self.masterMatchingObject, self.listingQueue, self.matchQueue, self.listingsProcessed, self.matches, self.ambiguous)

        threads.flagIfProcessingFinished(self.listingQueue, processes.stopProcesses, self.matchQueue, self)

    def printData(self):
        files.printProductMatches(self.productMatches, self.outputFileHandle)

        
