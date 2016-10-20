import time

class View():
    def __init__(self, model):
        self.model = model

        #ANSI Escape Codes 
        self.blue = "\u001b[34m"
        self.brightBlue = "\u001b[34;1m"
        self.cyan = "\u001b[36m"
        self.brightCyan = "\u001b[36;1m"
        self.green = "\u001b[32;1m"

        self.bold = "\u001b[1m"

        self.reset = "\u001b[0m"
        self.clearLine = "\u001b[2]"
        self.up = "\u001b[1A"
        self.down = "\u001b[1B"
        self.beginningOfLine = "\u001b[200D"

        self.startTime = 0

    def start(self):
        print("Starting Processing")
        self.startTime = time.time()
        
        self.model.startLookingForMatches()
        self.updateProgress()
        self.printSummary()
        
        print("Writing To File")

        self.model.printData()

        print("Finished Writing")

    def getProgressBar(self, listingsProcessed, totalListings):
        width = 20
        quarter = int(width / 4)
        distanceCovered = int((listingsProcessed / totalListings) * width)

        if distanceCovered == width:
            colour = self.green
        elif distanceCovered >= width - quarter:
            colour = self.brightCyan
        elif distanceCovered >= width - quarter * 2:
            colour = self.cyan
        elif distanceCovered >= width - quarter * 3:
            colour = self.blue
        else:
            colour = self.brightBlue

        return "[{}{:{}}{}]".format(colour, ">" * distanceCovered, width, self.reset)

    def printSummary(self):
        totalListings = self.model.listingsProcessed.value
        
        print("Match:     {:>6} ({:.0%})".format(self.model.matches.value, self.model.matches.value / totalListings))
        print("Ambiguous: {:>6} ({:.0%})".format(self.model.ambiguous.value, self.model.ambiguous.value / totalListings))
        print("No Match:  {:>6} ({:.0%})".format(totalListings - (self.model.matches.value + self.model.ambiguous.value), (totalListings - (self.model.matches.value + self.model.ambiguous.value)) /totalListings))
    
    def getTime(self):
        runTime = time.time() - self.startTime
        return "({:02.0f}:{:02.0f})".format(runTime // 60, runTime % 60)

    def getProcessingCount(self, listingsProcessed, totalListings):
        return "{:6d}/{:<6d}".format(listingsProcessed, totalListings)

    def getProcessingPercentage(self, listingsProcessed, totalListings):
        percentage = listingsProcessed / totalListings
        
        if percentage < 100.0:  
            return "{:3.0%}".format(percentage)
        else:
            return "{}{:3.0%}{}".format(self.bold, percentage, self.reset)

    def printProcessingOutput(self, listingsProcessed, totalListings, lastLine=False):
        print("{}{:22} {:7}".format(self.beginningOfLine,
                                    self.getProgressBar(listingsProcessed, totalListings),
                                    self.getTime()), end="\r")
        print(self.down, end="\r")
        print("{}{:11}     {:4}".format(self.beginningOfLine,
                                        self.getProcessingCount(listingsProcessed, totalListings),
                                        self.getProcessingPercentage(listingsProcessed, totalListings)), end="\r")
        if lastLine:
            print("")
        else:
            print(self.up, end="\r")
    
    def updateProgress(self):
        print("")
        print(self.up, end="\r")
        
        while self.model.currentlyProcessing:
            self.printProcessingOutput(self.model.listingsProcessed.value, self.model.totalListings)
            time.sleep(0.1)
            
        self.printProcessingOutput(self.model.listingsProcessed.value, self.model.totalListings, lastLine=True)

