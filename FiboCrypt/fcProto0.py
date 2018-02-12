# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import math

from random import random

from datetime import datetime

fibArr = []
fibArrInit = False

def initFibArr(n = 20):
    global fibArr
    global fibArrInit
    fibArrInit =True
    p = 1
    q = 1
    for i in range(n):
        tmp = q
        q += p
        p = tmp
        fibArr.append(p+q)

def fiboCryptUnicode(text, p, q):
    mList = fibocrypt(text, p, q)
    leftMask = int('11111111111111110000000000000000', 2)
    rightMask = int('00000000000000001111111111111111', 2)
    uniText = u''
    for matrix in mList:
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                num = matrix[i, j]
                # testing....
#
#                if num < 0:
#                    num = (~num) + 1

                left = (num & leftMask) >> 16
                right = num & rightMask
                uniText += chr(left)+chr(right)
                print(str(num) + '=' + chr(left)+chr(right))
                print(bin(num) + '=' + bin(left)+bin(right)+'||'+bin((left<<16)|right)+'|'+str((left<<16)|right))
        uniText += u',' + chr(int(random()*10000))
    return uniText


def fibocrypt(text, p, q):
    global fibArrInit

    if not fibArrInit:
        initFibArr()

    r = p+q
    txtLen = len(text)
    rem = txtLen % 3
    divF = txtLen//3

    if rem != 0:
        divF += 1

    for i in range(rem):
        text += '\0'

    txtLen = len(text)

    ## The list of matrices containting CryptText
    matList = []

    for i in range(0, txtLen - 1, 3):
        try:
            a = ord(text[i])
        except(ValueError, IndexError):
            a = 0

        try:
            b = ord(text[i+1])
        except(ValueError, IndexError):
            b = 0

        try:
            c = ord(text[i+2])
        except(ValueError, IndexError):
            c = 0

        M = np.matrix('1 0 0; '+ str(a) +' 1 0; '+ str(b) +' '+ str(c) +' 1', dtype=object)
        I = np.matrix('1 0 0; 0 1 0; 0 0 1', dtype = object)
        D = np.matrix(str(p) +' 0 0; 0 ' + str(q) + ' 0; 0 0 ' + str(r), dtype=object)
        X = (2*I - M.transpose())
        C = M * D * X

        matList.append(C)
#        print('M:\n'+str(M)+'\nI:\n'+str(I)+'\nX:\n'+str(X)+'\n=========='+'\nC:\n'+str(C))

    return matList

def decryptList(mList, p, q):
    text = ''
    for i in mList:
        text += deFibo(i, p, q)

    return text


def decryptUnicode(text, p, q):
    negMask = 1 << 31
    textLen = len(text)
    mList = []
    currList = []
    currElemCount = 0
    for i in range(0, textLen, 2):
        if text[i] == ',':
            rank = 3
#            rank = int(math.sqrt(currElemCount))
            temp = []
            for j in range(rank):
                temp_ = []
                for k in range(rank):
                    temp_.append(currList[((j*rank) + k)])
                temp.append(temp_)

            matrix = np.matrix(temp, dtype=object)
            mList.append(matrix)

            currList = []
            currElemCount = 0

        left = ord(text[i]) << 16
        right = ord(text[i+1])
        num = left | right


        currList.append(num)

        currElemCount += 1

    return decryptList(mList, p, q)


def verify(M):
    mList = M.tolist()
    m1List = [mList[0][0]]
    m2List = [[mList[0][0], mList[0][1]],[mList[1][0], mList[1][1]]]
    m3List = mList
    d1 = np.linalg.det(np.matrix(m1List))
    d2 = np.linalg.det(np.matrix(m2List))
    d3 = np.linalg.det(np.matrix(m3List))

    return (d1 + d2) == d3


def deFibo(M, p, q):
    dim = M.shape
    if dim[0] != dim[1]:
        print('error! the matrix is not square!')
        return None

    pInv = -1/p
#    a = int(pInv*M[0,1])
#    b = int(pInv*M[0,2])
    a = int(round(pInv*M[0,1]))
    b = int(round(pInv*M[0,2]))
#    c = int(1/q * (-1*p*a*b - M[1,2]))
    c = int(round(-1*p*a*b - M[1,2])/q)
#    print('a=' + str(a) + ', b=' + str(b) + ', c=' + str(c))
    return chr(a) + chr(b) + chr(c)


def main():
    print('FiboCrypt-0.01 (Pre-Alpha)\n')
    print('MENU\n')
    print('1 - Encrypt in matrix Form')
    print('2 - Encrypt 1k sample')
    print('3 - Encrypt 64k sample')
#    print('2 - Encrypt in Unicode')
    print('4 - Exit\n')

    menuResponse = int(input('Enter your MENU choice: '))
#    menuResponse = 1
    initFibArr()
    time2 = None

    if menuResponse == 1:
        text = input('Enter Text: ')
    if menuResponse == 2 or menuResponse == 3:
        text = ''
        if menuResponse == 2:
            with open('text1k.txt') as f:
                for line in f:
                    text += line
        if menuResponse == 3:
            with open('text64k.txt') as f:
                for line in f:
                    text += line

#            text = text * 64

    p = 43566776258855008468992
    q = 43566776258855008468992

    print('Using p = ' + str(p) + ', q = ' + str(q))

    time1 = datetime.now()

    cryptList = fibocrypt(text, p, q)

    time2 = datetime.now()
    diff1 = time2 - time1

    print('CipherText:\n'+str(cryptList))


    time1 = datetime.now()
    print('Text after decryption: ' + decryptList(cryptList, p, q))
    time2 = datetime.now()
    diff2 = time2 - time1
    print('String Length: ' + str(len(text)))
    print('Time elapsed encode: ' + str(diff1.microseconds) + ' \u03bc sec')

    print('Time elapsed decode: ' + str(diff2.microseconds) + ' \u03bc sec')
#    elif menuResponse == 2:
#        text = input('Enter Text: ')
#        cryptText = fiboCryptUnicode(text, 5, 8)
#        print('CipherText:\n'+str(cryptText))
#        print('Text after decryption: ' + decryptUnicode(cryptText, 5, 8))




if __name__ == '__main__':
    main()
