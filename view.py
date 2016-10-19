import time

class View():
    def __init__(self, model):
        self.model = model

        #ANSI Escape Codes 
        self.blue = "\u001b[34m"
        self.brightBlue = "\u001b[34;1m"

        self.bold = "\u001b7m"

    def start(self):
        print("Starting Processing")
        self.model.startLookingForMatches()
        self.updateProgress()
        print("Finished Processing")
        print("Writing To File")
        self.model.printData()
        print("Finished Writing")
        
    def updateProgress(self):
        while self.model.currentlyProcessing:
            print("Processing {} of {}  {}".format(self.model.listingsProcessed.value, self.model.totalListings, "True" if self.model.currentlyProcessing else "False"), end="\r")
            time.sleep(0.1)
        print("Processing {} of {}  {}".format(self.model.listingsProcessed.value, self.model.totalListings, "True" if self.model.currentlyProcessing else "False"))
