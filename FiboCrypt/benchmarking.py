# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 23:04:56 2017

@author: abhi
"""

from fcProto0 import fibocrypt, decryptList
from datetime import datetime

def readTextFile():
    with open('text.txt', 'r') as file:
        data = file.readline()

    return data


text = readTextFile()

itr = 1

avgEncryptTime = 0
avgDecryptTime = 0

print('Testing for 65536 characters')

for i in range(itr):
#    print(i)
    time1 = datetime.now()
    l = fibocrypt(text, 2880067194370824704, 4660046610375544832)
    time2 = datetime.now()
    avgEncryptTime += (time2-time1).microseconds
    time1 = datetime.now()
    decryptList(l, 2880067194370824704, 4660046610375544832)
    time2 = datetime.now()
    avgDecryptTime += (time2-time1).microseconds

avgEncryptTime //= itr
avgDecryptTime //= itr

print('Average Encrypt Time: ' + str(avgEncryptTime) + ' \u03bc sec')
print('Average Decrypt Time: ' + str(avgDecryptTime) + ' \u03bc sec')
