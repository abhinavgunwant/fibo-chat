import math
import random

# def round(n):
#     integer = int(n)
#     if(int(n) - )

def fibNo(n):
    # phi = 1.61803398874989484820
    # phi_ = -0.61803398874989484820
    # phi_ = phi - 1
    # return int((phi**n - (-1*phi_)**n)/math.sqrt(5))
    # return int((phi**n - (phi_)**n)/math.sqrt(5))
    return int(((1.61803398874989484820)**n - (-0.61803398874989484820)**n)/2.23606797749979)

def randomInt(digits):
    # itr = 0
    # ten = '10'
    # zero = '0'
    # while True:
    #     dig = 10 ** (digits + itr)
    #     # dig = int(ten + zero ** (digits+itr-1))
    #     rNo = random.random()
    #     no = int(rNo * dig)
    #     if len(str(no)) == digits:
    #         break
    #     itr += 1
    
    # return no
    return int((random.random())*(10**digits))