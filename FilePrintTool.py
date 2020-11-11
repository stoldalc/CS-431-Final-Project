# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 21:54:17 2020

@author: Christian
"""


AmazonDataFP = open("amazon-meta.txt","r",encoding="utf8")

fileText = AmazonDataFP.readlines()

"""
PrintNLines = 4650

for i in range(PrintNLines):
    print(fileText[i],end='')
    
"""    

shouldPrint = 0;


startLine = 'Id:   0\n'

endLine = 'Id:   11\n'

for i in range(len(fileText)):
    if(fileText[i] == startLine):
        shouldPrint = 1
    
    if(fileText[i] == endLine):
        shouldPrint = 0
    
    if(shouldPrint == 1):
        print(fileText[i])
    
    
    