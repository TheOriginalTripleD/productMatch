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
    def __init__(self, products, productToListingMap, requiredFields, desiredFields, accuracy):
        self.products = products
        self.productToListingMap = productToListingMap
        self.productTree = createProductTree(products, *(requiredFields + desiredFields))

        self.requiredFields = self.fieldsSortedByMemberCount(requiredFields)
        self.desiredFields = self.fieldsSortedByMemberCount(desiredFields)

        self.accuracy = accuracy
  
    def fieldsSortedByMemberCount(self, fields):
        return sorted(fields, key=lambda field: len(self.productTree[field]))

    def fieldValueContainsString(self, fieldValue, searchString):
        if fieldValue == "null":
            return False
        return re.search("(^| ){}($| )".format(searchString.lower()), fieldValue.lower())

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
            chosenProductIndex = -1
            
        return chosenProductIndex
