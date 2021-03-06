"""
Created on Sun Nov  1 21:54:17 2020

@author: Christian
"""
import pyparsing as pp
from pyparsing import Literal
import time as timer
from pathlib import Path


amazonMetaFile =  Path("amazon-meta.txt")
ASINListFile = Path('D:\Media\Documents\Edumacate\FALL 2020\CS 431\Amazon data set\CS-431-Final-Project\Lists\ASINList.txt')
CategoriesListFile = Path('D:\Media\Documents\Edumacate\FALL 2020\CS 431\Amazon data set\CS-431-Final-Project\Lists\CategoriesList.txt')
CunsomerIDListFile = Path('D:\Media\Documents\Edumacate\FALL 2020\CS 431\Amazon data set\CS-431-Final-Project\Lists\CunsomerIDList.txt')
ReviewsWithASINFile = Path('D:\Media\Documents\Edumacate\FALL 2020\CS 431\Amazon data set\CS-431-Final-Project\Lists\ReviewsWithASIN.txt')


CustomerIDSet = set()
CategoriesSet = set()
ASINSet = set()
ReviewsWithASIN = []




def IDLineFunction(s):
    result = ''
    for i in range(5,len(s)):
        result += s[i]
    #print("Current ID is: " + result)
    return result

def ASINLineFunction(s):
    result = ''
    global ASINSet
    for i in range(5,len(s)):
        result += s[i]
        
    result = result [:-1]
    ASINSet.add(result)
    return result

def TitleLineFunction(s):
    result = ''
    for i in range(8,len(s)):
        result += s[i]   
    return result

def GroupLineFunction(s):
    result = ''
    for i in range(8,len(s)):
        result += s[i]   
    return result

def SalesRankLineFunction(s):
    result = ''
    for i in range(12,len(s)):
        result += s[i]      
    return result

def SimilarLineFunction(s):
    result = ''
    for i in range(11,len(s)):
        result += s[i]
    return result
    
def NumOfCategoriesFinder(s):
    result = ''

    for i in range(13,len(s)):
        result += s[i]
    return int(result)

def categoriesParser(s):
    buffer = ''
    result = []
    
    #print("Categories is currently parsing the line: ")
    #print(s)
    
    for i in range(4,len(s)):
        
        global CategoriesSet
        if(s[i] == '\n'):
            break
        
        if(s[i] == '|'):
            result.append(buffer)
            CategoriesSet.add(buffer)
            i+=1
            #print("Appended the category: " + buffer)
            buffer = ''
        else:
            buffer += s[i]
        
    return result
        
        


def NumOfReviewsFinder(s):
    result = ''
    i = 18
    while s[i] != ' ':
        result += s[i]
        i += 1
    #print("\t***Number of reviews for this product is: ***" + result)
    return int(result)




def ReviewsParser(s, cASIN):
    #print("Attempting to parse the following line: ")
    #print("->" + s + "<-")
    global CustomerIDSet
    global ReviewsWithASIN
    reviewFormat = (pp.Word(pp.nums+'-') + 
          Literal('cutomer:').suppress() + pp.Word(pp.alphanums) + 
          Literal('rating:').suppress() + pp.Word(pp.nums) + 
          Literal('votes:').suppress() + pp.Word(pp.nums) + 
          Literal('helpful:').suppress() + pp.Word(pp.nums))
    reviewB = reviewFormat.parseString(s)
    #print(reviewB)
    #print(reviewFormat.searchString(s))
    
    if reviewB != '':
         CustomerIDSet.add(reviewB[1])
         reviewB.insert(0,cASIN)
         ReviewsWithASIN.append(reviewB)
    
    return reviewB
    
def timeAvg(s):
    
    totalTime = 0
    for i in range(len(s)):
        totalTime += s[i]
    return round(totalTime/len(s),2)
    

#Reading in the Amazon Co-purchase dataset

Start = timer.perf_counter()
AmazonDataFP = open(amazonMetaFile,"r",encoding="utf8")
fileText = AmazonDataFP.readlines()
Stop = timer.perf_counter()
AmazonDataFP.close()
print("Reading in meta data and converting to str arr took: " + str(round(Stop-Start,2)) + "secs")

IDCount = 0
isAnIDLine = fileText[0]
count = 0



IDs = []
ASINs = []
Titles = []
Groups = []
SalesRanks = []
Similars = []
Categories = []
Reviews = []

discontunedProductsCount = 0;


testingLines = 10000
timeAverages = []

#Parsing all the lines of the txt file and seperating into diffrent arrs
Start = timer.perf_counter()
StartOfMil = Start
#for i in range(len(fileText)):
for i in range(testingLines):
    isAnIDLine = fileText[i]
    
    if(((i%100000) == 0) & (i > 0)):
        Lap = timer.perf_counter()
        print("----------------------------------------------------------------------------")
        print("Current line: " + str(i) + " of " + str(len(fileText)))
        timeBuffer = Lap-StartOfMil
        StartOfMil = Lap
        timeAverages.append(timeBuffer)
        print("It took " + str(round(timeBuffer,2)) + "secs to read 100000 lines")
        print("Currently avg " + str(timeAvg(timeAverages)) + "secs per 100000 lines")
        print("With a total elapsed time of " + str(round(Lap-Start,2)) + "secs for "  + str(i) + " lines")
        print("----------------------------------------------------------------------------")
    if(isAnIDLine[0] == 'I'):
        #print(isAnIDLine)
        IDCount += 1
        IDs.append(IDLineFunction(isAnIDLine))
        
        i += 1
        ASINs.append(ASINLineFunction(fileText[i]))
        currentASIN = ASINLineFunction(fileText[i])
        i += 1
        #print(fileText[i])
        if(fileText[i] == '  discontinued product\n'):
            #print("  discontinued product at line: " + str(i))
            discontunedProductsCount += 1
            Titles.append('')
            Groups.append('')
            SalesRanks.append('')
            Similars.append('')
            emptyList = ['']
            Categories.append(emptyList)
            Reviews.append(emptyList)
        else:
            Titles.append(TitleLineFunction(fileText[i]))
            i += 1
            Groups.append(GroupLineFunction(fileText[i]))
            i += 1
            SalesRanks.append(SalesRankLineFunction(fileText[i]))
            i += 1
            Similars.append(SimilarLineFunction(fileText[i]))
            i += 1
            CategoriesList = []
            for j in range(NumOfCategoriesFinder(fileText[i])): 
                i += 1
                CategoriesList.append(categoriesParser(fileText[i]))
            Categories.append(CategoriesList)
            
            i += 1
            ReviewsList = []
            CurrentItemNumberOfReviews = NumOfReviewsFinder(fileText[i])
            for j in range(CurrentItemNumberOfReviews):
                i += 1
                #ReviewsList.append(fileText[i])
                if(fileText[i] != '\n'):
                    ReviewsList.append(ReviewsParser(fileText[i],currentASIN))
                else:
                    #print("Empty Line Found")
                    #j = CurrentItemNumberOfReviews+1
                    break
                    
                #print("Number of revies recorded for current item is: " + str(len(ReviewsList)))
            Reviews.append(ReviewsList)
            
totalDataParseTime = timer.perf_counter()




#Printing customer ID list to txt file

print("Creating txt file containing customer ID lists")
IDTxtFileStart = timer.perf_counter()     
customerIDFile = open(CunsomerIDListFile,"w+")

for i in range(len(CustomerIDSet)):
    if(i % 10000) == 0:
        print("Customer ID current i is: " + str(i) + " out of " + str(len(CustomerIDSet)))
    IDBuffer = CustomerIDSet.pop() + '\n' 
    customerIDFile.write(IDBuffer)

customerIDFile.close()
IDTxtFileStop = timer.perf_counter()   
print("Creation of customer IDs txt file took: " + str(round(IDTxtFileStop-IDTxtFileStart,2)) + "secs" )


#Creating and printing ASINs to a txt file
ASINTxtFileStart = timer.perf_counter()     
ASINFile = open(ASINListFile,"w+")

for i in range(len(ASINSet)):
    if(i % 10000) == 0:
        print("ASIN current i is: " + str(i) + " out of " + str(len(ASINSet)))
    ASINBuffer = ASINSet.pop() + '\n'
    ASINFile.write(ASINBuffer)

ASINFile.close()
ASINTxtFileStop = timer.perf_counter()   
print("Creation of ASIN txt file took: " + str(round(ASINTxtFileStop-ASINTxtFileStart,2)) + "secs" )


#Creating a txt file that contains all diffrent categories
CategoriesFileStart = timer.perf_counter()
CategoriesFile = open(CategoriesListFile,"w+")

for i in range(len(CategoriesSet)):
    if(i % 10000) == 0:
        print("Categories current i is: " + str(i) + " out of " + str(len(CategoriesSet)))
        
    CategoriesBuffer = CategoriesSet.pop() + '\n'
    CategoriesFile.write(CategoriesBuffer)

CategoriesFile.close
CategoriesFileStop = timer.perf_counter()
print("Categories file creation took: " + str(round(CategoriesFileStop-CategoriesFileStart,2)) + "secs" )

#Creating a txt file that contains all reviews with ASIN as first value
ReviewsASINStart = timer.perf_counter()
ReviewASINFile = open(ReviewsWithASINFile,"w+")

for i in range(len(ReviewsWithASIN)):
    if(i % 10000) == 0:
        print("ASIN andR reviews write current i is: " + str(i) + " out of " + str(len(ReviewsWithASIN)))
    for j in range(len(ReviewsWithASIN[i])):
        ReviewASINFile.write(ReviewsWithASIN[i][j] + ' ')
    #ReviewASINFile.write(ReviewsWithASIN[i])
    ReviewASINFile.write('\n')
    
ReviewASINFile.close
ReviewsASINStart = timer.perf_counter()
print("ASIN andR reviews write file creation took: " + str(round(CategoriesFileStop-CategoriesFileStart,2)) + "secs" )




print()
print()
print()

#print("Customer ID list:")
#print(customerIDList)

print()
print()
print()


print("Id arr size is: " + str(len(IDs)))
print("ASIN arr size is: " + str(len(ASINs)))
print("Title arr size is: " + str(len(Titles)))
print("Group arr size is: " + str(len(Groups)))
print("SalesRank arr size is: " + str(len(SalesRanks)))
print("Similiar arr size is: " + str(len(Similars)))
print("Categories arr size is: " + str(len(Categories)))
print("Reviews arr size is: " + str(len(Reviews)))
#print("CustomerIDList size is: " + str(len(customerIDList)))
print('Number of discontinued products is: ' + str(discontunedProductsCount))
