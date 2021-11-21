#!/usr/bin/env python3

from argparse import ArgumentParser
from sys import argv
from enchant import Dict as dicnary

#pip3 install pyenchant

class caesar:
    # setting the data
    def __init__(self,plainText=None, encryptedText=None, key=3 ):
        self.plainText = plainText
        self.encryptedText = encryptedText
        self.key = key
        self.dictionary = dicnary("en_US")
    
    def encrypt(self, plainText=None , encryptionKey=None):
        # set the default plaintext if none is passed
        if plainText is None :
            plainText = self.plainText
        result = []
        for i in plainText:
            if i.islower():
                indexOfI = ord(i) - ord("a") # act like the normal index a = 0 , b = 1
                newI = ( indexOfI + encryptionKey ) % 26 + ord("a") # restore the ascii 
                result.append(chr(newI))
            elif i.isupper():
                indexOfI = ord(i) - ord("A") 
                newI = ( indexOfI + encryptionKey ) % 26 + ord("A")
                result.append(chr(newI))
            elif i.isspace():
                result.append(" ")
            elif i.isdigit():
                newI = (int(i) + encryptionKey) % 10 # just shift the number then add the new shifted
                result.append(newI)
            else:
                result.append(i)
        return "".join(str(x) for x in result)

    def decrypt(self, decryptionKey, encryptedText=None ):
        # set the class encryptedText if none is passed
        if encryptedText is None :
            encryptedText = self.encryptedText
        result = []
        for i in encryptedText:
            if i.islower():
                indexOfI = ord(i) - ord("a") # act like the normal index a = 0 , b = 1
                newI = ( indexOfI - decryptionKey ) % 26 + ord("a") # restore the ascii 
                result.append(chr(newI))
            elif i.isupper():
                indexOfI = ord(i) - ord("A") 
                newI = ( indexOfI - decryptionKey ) % 26 + ord("A")
                result.append(chr(newI))
            elif i.isspace():
                result.append(" ")
            elif i.isdigit():
                newI = (int(i) - decryptionKey) % 10 # just shift the number then add the new shifted
                result.append(newI)
            else:
                result.append(i)
        return "".join(str(x) for x in result)

    # return array of key and it's result [[1,"Text"],[2,"Text"]]
    def bruteForce(self, encryptedText=None):
        if encryptedText is None: # if no encrypted text is passed assig the class self
            encryptedText = self.encryptedText
        result = []
        for i in range(27): # all possible keys
            result.append([i,self.decrypt(i,encryptedText=encryptedText)])
        else:
            return result # return the result array after finishing the loop

    # if it's mixed with numbers Gives False
    def isEnglish(self,text):
        return self.dictionary.check(text)
    
    def findUsedKey(self,bruteForceResult):
        for key , text in bruteForceResult:
            if cipherText.isEnglish(text):
                return [key,text]

# Help message - how to use the script
help="\n-encrypt [text] -key [key]\n-decrypt [cipher] -key [key]\n-bruteForce [ Encrypted Text]"

if __name__ == "__main__":
    #parser = ArgumentParser()
    if len(argv) < 3:
        print(help)
        #print(argv)
        exit()
    elif argv[1] == "-encrypt" and argv[3] == "-key":
        plainText = argv[2]
        key = int(argv[4])
        cipherText = caesar(plainText=plainText , key=key)
        print(cipherText.encrypt(encryptionKey=key))
    elif argv[1] == "-decrypt" and argv[3] == "-key":
        encryptedText = argv[2]
        key = int(argv[4])
        cipherText = caesar(encryptedText=encryptedText , key=key)
        print(cipherText.decrypt(key))
    elif argv[1] == "-bruteForce":
        encryptedText = argv[2]
        cipherText = caesar(encryptedText=encryptedText)
        bruteForceResult= cipherText.bruteForce()
        resultKey = cipherText.findUsedKey(bruteForceResult)
        print("Key",resultKey[0],"Gives",resultKey[1])
    else:
        print(help)
    