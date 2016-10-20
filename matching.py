import re

def createProductTree(products, *fields):
    #Creates an organized "tree" of products. The keys are the
    #"fieldTitles" (e.g. "manufacturer", "model", etc.) which
    #contain a dict of "fieldValues" (e.g. "Samsung", "X510", etc.).
    #Each fieldValue points to a list of numbers which are the
    #indices of products in the product table which contain that
    #fieldValue
    
    tree = {fieldTitle: {"null": [] } for fieldTitle in fields}

    for index, product in enumerate(products):
        for fieldTitle in fields:
            if fieldTitle not in product:
                tree[fieldTitle]["null"].append(index)
            elif product[fieldTitle].lower() in tree[fieldTitle]:
                tree[fieldTitle][product[fieldTitle].lower()].append(index)
            else:
                tree[fieldTitle][product[fieldTitle].lower()] = [index]
    return tree

class Matching():
    requiredFields = ["manufacturer", "model"]
    desiredFields = ["family"]
    productToListingMap = {"model": "title",
                           "family":"title",
                           "manufacturer":"manufacturer"}
    
    def __init__(self, products):
        self.products = products
        
        self.productTree = createProductTree(products, *(self.requiredFields + self.desiredFields))

        self.requiredFields = self.fieldsSortedByMemberCount(self.requiredFields)
        self.desiredFields = self.fieldsSortedByMemberCount(self.desiredFields)

        self.regularExpression = "(^| |_|-|,){}($| |_|-|,)"

        #Listings may use '_', '-', or "" in place of a blank space, so we search for all 3
        self.separators = [" ", "_", "-", ""]

    def copy(self):
        return Matching(self.products)
        
    def fieldsSortedByMemberCount(self, fieldTitle):
        return sorted(fieldTitle, key=lambda fieldTitle: len(self.productTree[fieldTitle]))

    def splitValueBySeparators(self, partition, separators):
        if not separators:
            return [partition]

        separator = separators.pop()

        #'split' cannot handle an empty separator, so we create a special case
        subPartitions = partition.split(separator) if separator else [partition]

        listOfPartitions = list()
        
        for partition in subPartitions:
            listOfPartitions += self.splitValueBySeparators(partition, separators)

        return listOfPartitions

    def getPartitionPermutations(self, partitions, valuePermutation=""):
        if len(partitions) == 1:
            return [partitions.pop() + valuePermutation]

        partition = partitions.pop()
        permutationsList = list()
        
        for separator in self.separators:
            permutationsList += self.getPartitionPermutations(list(partitions), separator + partition + valuePermutation)

        return permutationsList
            
    def allFieldValuePermutations(self, fieldValue):
        #Returns a set of all the possible permutations a fieldValue
        #could have based on its separators. e.g. ["EX-H20G", "EX H20G",
        #"EX_H20G", etc,]
        partitions = self.splitValueBySeparators(fieldValue, list(self.separators))
        return self.getPartitionPermutations(partitions)
        
        
    def fieldValueContainsString(self, fieldValue, searchString):
        if fieldValue == "null":
            return False

        test =  self.allFieldValuePermutations(searchString)
        
        for permutation in test:
            match = re.search(self.regularExpression.format(permutation.lower()),
                              fieldValue.lower())
            if match:
                break

        return match
                

    def matchingProducts(self, fieldTitle, listing):
        productIndexSet = set()

        for fieldValue in self.productTree[fieldTitle]:
            if self.fieldValueContainsString(listing[self.productToListingMap[fieldTitle]], fieldValue):
                productIndexSet = productIndexSet.union(set(self.productTree[fieldTitle][fieldValue]))

        return productIndexSet
#        return {productIndex for fieldValue in self.productTree[fieldTitle] if self.fieldValueContainsString(listing[self.productToListingMap[fieldTitle]], fieldValue) for productIndex in self.productTree[fieldTitle][fieldValue]} 

    def productsWithRequiredFields(self, fields, listing):
        fieldTitle = fields.pop()

        if not fields:
            return self.matchingProducts(fieldTitle, listing)

        matchingRows = self.productsWithRequiredFields(fields, listing)

        if matchingRows:
            return matchingRows & self.matchingProducts(fieldTitle, listing)

        return matchingRows

    def productHasFieldTitle(self, productIndex, fieldTitle):
        return True if fieldTitle in self.products[productIndex] else False

    def bestMatch(self, weightedProducts):
        if len(weightedProducts) <= 1:
            return weightedProducts[0][1]

        weightedProducts.sort(key=lambda score: score[0], reverse=True)

        #If there is a tie between the best and second-best match, err on the side of caution
        #and return None
        return weightedProducts[0][1] if weightedProducts[0][0] != weightedProducts[1][0] else -1

    def findBestMatch(self, productIndices, listing):
        #Assigns a weight to each product index. Weight is incremented for each match with the listing
        weightedProducts = [[0, index] for index in productIndices]

        for pair in weightedProducts:
            for fieldTitle in self.desiredFields:
                if (self.productHasFieldTitle(pair[1], fieldTitle) and
                    self.productToListingMap[fieldTitle] in listing and
                    self.fieldValueContainsString(listing[self.productToListingMap[fieldTitle]], self.products[pair[1]][fieldTitle])):
                        pair[0] += 1

        return self.bestMatch(weightedProducts)
    
    def findMatchingProduct(self, listing):
        matchingProducts = self.productsWithRequiredFields(list(self.requiredFields), listing)
        
        if matchingProducts:
            chosenProductIndex = self.findBestMatch(matchingProducts, listing)
        else:
            chosenProductIndex = -2
            
        return chosenProductIndex
