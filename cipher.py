#!/usr/bin/env python3

from argparse import ArgumentParser
from sys import argv

class caesar:
    # setting the data
    def __init__(self,plainText=None, encryptedText=None, key=3 ):
        self.plainText = plainText
        self.encryptedText = encryptedText
        self.key = key
        self.dictionary = {ascii:chr(ascii) for ascii in range(128)}
    
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

    def bruteForce(self, encryptedText):
        pass


help="\n-encrypt [text] -key [key]\n-decrypt [cipher] -key [key]\n"

if __name__ == "__main__":
    #parser = ArgumentParser()
    if len(argv) != 5:
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
    else:
        print(help)
    