import numpy as np
import math

from random import random

from datetime import datetime

def fibocrypt(text, p, q):
    global fibArrInit

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

    return matList

def decryptList(mList, p, q):
    text = ''
    for i in mList:
        text += deFibo(i, p, q)

    return text

def verify(M):
    mList = M.tolist()
    m1List = [mList[0][0]]
    m2List = [[mList[0][0], mList[0][1]],[mList[1][0], mList[1][1]]]
    m3List = mList
    a = mList[0][0]
    b = mList[0][1]
    c = mList[0][2]
    d = mList[1][0]
    e = mList[1][1]
    f = mList[1][2]
    g = mList[2][0]
    h = mList[2][1]
    i = mList[2][2]

    d1 = a
    d2 = a * e - b * d
    d3 = a*(e*i - f*h) - b*(d*i - f*g) + c*(d*h - e*g)

    print('d1: ' + str(d1) + ' d2: ' + str(d2) + ' d3: ' + str(d3) + ' d1+d2=' + str(d1+d2))

    return (d1 + (d2/d1)) == (d3/d2)

def verifyAll(cryptList):
    for i in cryptList:
        if verify(i) == False:
            return False
    return True

def deFibo(M, p, q):
    dim = M.shape
    if dim[0] != dim[1]:
        print('error! the matrix is not square!')
        return None

    pInv = -1/p
    a = int(round(pInv*M[0,1]))
    b = int(round(pInv*M[0,2]))
    c = int(round(-1*p*a*b - M[1,2])/q)
    return chr(a) + chr(b) + chr(c)

def toString(matList,p,q):
    text = str(p) + ',' + str(q) + ','

    for mat in matList:
        text += (str(mat[0,0]) + ',' + str(mat[0,1]) + ',' + str(mat[0,2]) + ','
                    + str(mat[1,0]) + ',' + str(mat[1,1]) + ',' + str(mat[1,2]) + ','
                    + str(mat[2,0]) + ',' + str(mat[2,1]) + ',' + str(mat[2,2]) + ',')


    return text[:-1]

def fromString(text, psk):
    numbers = text.split(',')

    if psk == None:
        psk = {'p':0, 'q':0}

    p = int(numbers[0]) + psk['p']
    q = int(numbers[1]) + psk['q']

    cryptList = []

    for i in range(2, len(numbers), 9):
        cryptList.append(
            np.matrix(
                numbers[i] + ' ' + numbers[i+1] + ' ' + numbers[i+2] + '; ' +
                numbers[i+3] + ' ' + numbers[i+4] + ' ' + numbers[i+5] + ';' +
                numbers[i+6] + ' ' + numbers[i+7] + ' ' + numbers[i+8]
            )
        )

    return (cryptList, p, q)

def decryptFromString(text, psk):
    cryptList, p, q = fromString(text, psk)

    return decryptList(cryptList, p, q)

def main():
    print('FiboCrypt-0.01 (Pre-Alpha)\n\nMENU\n')
    print('1 - Encrypt in matrix Form\n2 - Encrypt 1k sample')
    print('3 - Encrypt 64k sample\n4 - Exit\n')

    menuResponse = int(input('Enter your MENU choice: '))
    # initFibArr()
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

    p = 43566776258855008468992
    q = 70492524767089384226816

    print('Using p = ' + str(p) + ', q = ' + str(q))

    time1 = datetime.now()

    cryptList = fibocrypt(text, p, q)

    time2 = datetime.now()
    diff1 = time2 - time1

    print('CipherText:\n'+str(cryptList))

    print('Verifying crypted text....')
    if verifyAll(cryptList):
        print('verified!')
    else:
        print('not verified!')

    time1 = datetime.now()
    print('Text after decryption: ' + decryptList(cryptList, p, q))
    time2 = datetime.now()
    diff2 = time2 - time1
    print('String Length: ' + str(len(text)))
    print('Time elapsed encode: ' + str(diff1.microseconds) + ' \u03bc sec')
    print('Time elapsed decode: ' + str(diff2.microseconds) + ' \u03bc sec')

if __name__ == '__main__':
    main()
