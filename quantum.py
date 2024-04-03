#!/usr/bin/env python3

#########################
#                       #
#         Setup         #
#                       #
#########################

import argparse  # requires Python >= 3.2
import math
import sys
import textwrap

# adding your own S-box is as easy as adding an item to this dictionary
sboxes = dict()
sboxes['ctc2'] = [7, 6, 0, 4, 2, 5, 1, 3]
sboxes['present'] = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
sboxes['ascon'] = [4, 11, 31, 20, 26, 21, 9, 2, 27, 5, 8, 18, 29, 3, 6, 28, 30, 19, 7, 14, 0, 13, 17, 24, 16, 12, 1, 25,
                   22, 10, 15, 23]
sboxes['icepole'] = [31, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16,
                     19, 30, 25, 28, 0]
sboxes['keccak'] = [0, 5, 10, 11, 20, 17, 22, 23, 9, 12, 3, 2, 13, 8, 15, 14, 18, 21, 24, 27, 6, 1, 4, 7, 26, 29, 16,
                    19, 30, 25, 28, 31]
sboxes['ketje'] = sboxes['keccak']
sboxes['keyak'] = sboxes['keccak']
sboxes['primate'] = [1, 0, 25, 26, 17, 29, 21, 27, 20, 5, 4, 23, 14, 18, 2, 28, 15, 8, 6, 3, 13, 7, 24, 16, 30, 9, 31,
                     10, 22, 12, 11, 19]
sboxes['primate_inv'] = [1, 0, 14, 19, 10, 9, 18, 21, 17, 25, 27, 30, 29, 20, 12, 16, 23, 4, 13, 31, 8, 6, 28, 11, 22,
                         2, 3, 7, 15, 5, 24, 26]
sboxes['joltik'] = [14, 4, 11, 2, 3, 8, 0, 9, 1, 10, 7, 15, 6, 12, 5, 13]
sboxes['joltik_inv'] = [6, 8, 3, 4, 1, 14, 12, 10, 5, 7, 9, 2, 13, 15, 0, 11]
sboxes['lac'] = [14, 9, 15, 0, 13, 4, 10, 11, 1, 2, 8, 3, 7, 6, 12, 5]
sboxes['minalpher'] = [11, 3, 4, 1, 2, 8, 12, 15, 5, 13, 14, 0, 6, 9, 10, 7]
sboxes['prost'] = [0, 4, 8, 15, 1, 5, 14, 9, 2, 7, 10, 12, 11, 13, 6, 3]
sboxes['rectangle'] = [6, 5, 12, 10, 1, 14, 7, 9, 11, 0, 3, 13, 8, 15, 4, 2]
sboxes['rectangle_inv'] = [9, 4, 15, 10, 14, 1, 0, 6, 12, 7, 3, 8, 2, 11, 5, 13]
sboxes['Class13'] = [0, 8, 6, 13, 5, 15, 7, 12, 4, 14, 2, 3, 9, 1, 11, 10]
sboxes['Skinny'] = [12, 6, 9, 0, 1, 10, 2, 11, 3, 8, 5, 13, 4, 14, 7, 15]
sboxes['Skinny_inv'] = [3, 4, 6, 8, 12, 10, 1, 14, 9, 2, 5, 7, 0, 11, 13, 15]
sboxes['Fides'] = [1, 0, 25, 26, 17, 29, 21, 27, 20, 5, 4, 23, 14, 18, 2, 28, 15, 8, 6, 3, 13, 7, 24, 16, 30, 9, 31, 10,
                   22, 12, 11, 19]
sboxes['Fides_inv'] = [1, 0, 14, 19, 10, 9, 18, 21, 17, 25, 27, 30, 29, 20, 12, 16, 23, 4, 13, 31, 8, 6, 28, 11, 22, 2,
                       3, 7, 15, 5, 24, 26]
sboxes['x3'] = [0, 1, 8, 15, 12, 10, 1, 1, 10, 15, 15, 12, 8, 10, 8, 12]
sboxes['Prince'] = [11, 7, 3, 2, 15, 13, 8, 9, 10, 6, 4, 0, 5, 14, 12, 1]
sboxes['Gift'] = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
sboxes['Piccolo']=[14,4,11,2,3,8,0,9,1,10,7,15,6,12,5,13]
sboxes['Twine']=[12,0,15,10,2,11,9,5,8,3,13,7,1,14,6,4]
sboxes['Lblock']=[14,9,15,0,13,4,10,11,1,2,8,3,7,6,12,5]
sboxes['cipher']       = [4, 5, 0, 1, 12, 3, 10, 8, 6, 15, 7, 13, 14, 11, 9, 2]


#########################
#                       #
#    Helper functions   #
#                       #
#########################

#########################
#                       #
#          Main         #
#                       #
#########################

if __name__ == "__main__":
    # parsing command line input
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    # parser.add_argument('mode', metavar='mode', choices=['mc', 'bgc', 'gc', 'depth','AND-depth'], help="Mode to operate in. One of:\nmc     for multiplicative complexity\nbgc    for bitslice gate complexity\ngc     for gate complexity\ndepth  for depth complexity")
    parser.add_argument('cipher', metavar='cipher', choices=sorted(sboxes.keys()),
                        help="Name of cipher of which the S-box should be used. One of:\n" + textwrap.fill(
                            ', '.join(sorted(sboxes.keys())), 68))
    parser.add_argument('G', metavar='G', type=int, choices=range(1, 50), help=textwrap.fill(
        'Value to test for. E.g. number of nonlinear gates for mode=mc, circuit depth for mode=depth, etc.', 68))
    # parser.add_argument('width', metavar='width', nargs='?', type=int, choices=range(1, 50), help=textwrap.fill('Only applicable to mode=depth. Set width of circuit layer to test for.', 68))
    parser.add_argument('T', metavar='T', nargs='?', type=int, choices=range(1, 50),help=textwrap.fill(' .',68))
    # parser.add_argument('WFD', metavar='WFD', nargs='?', type=int, choices=range(1, 50),help=textwrap.fill('.', 68))
    args = parser.parse_args()

    # initialize globals using command line input
    sbox = sboxes[args.cipher]
    n = m = int(math.log(len(sbox),
                         2))  # currently only considering square S-boxes, but it also works if you set n and m to different values
    x = y = 0  # rename these, but ...

    for i in range(len(sbox) * n):
        print('x_{:d},y_{:d}'.format(i, i) + ':BITVECTOR(1);')
    g = args.G
    for i in range(1,g+1):
        for j in range(0,3):
            print('b{:d}_{:d},'.format(i,j),end='')
    print('b:BITVECTOR(1);')
    for i in range(1,g+1):
        for j in range(0,3*n):
            print('a{:d}_{:d},'.format(i,j),end='')
    print('a:BITVECTOR(1);')
    for i in range(0,len(sbox)):
        for j in range(1,args.G+1):
            for k in range(0,3):
                print('q{:d}_{:d}_{:d},'.format(i, j, k), end='')
    print('q:BITVECTOR(1);')
    for i in range(0,len(sbox)):
        for j in range(1,args.G+1):
            print('t{:d}_{:d},'.format(i,j),end='')
    print('t:BITVECTOR(1);')
    for i in range(0, g + 1):
        for j in range(len(sbox) * n):
            print('x{:d}_{:d},'.format(i, j), end='')
    print('x:BITVECTOR(1);')
    for i in range(0, 4):
        for j in range(0, 4):
            print('k{:d}_{:d},'.format(i, j), end='')
    print('k:BITVECTOR(1);')

    for l in range(len(sbox)):
        a = b = c = 0  # ... leave these the same
        # initially, let Z contain input bits
        Z = [str(x + _x) for _x in range(n)]

        for g in range(1, args.G + 1):
            a = 0
            for r in range(0,3):
                print('ASSERT(q{:d}_{:d}_{:d}=BVPLUS(1'.format(l, g, r ),end='')
                for z in Z:
                    print(',BVMULT(1,a{:d}_{:d},x{:d}_{:s})'.format(g,a,g-1,z),end='')
                    a=a+1
                print('));')
            print('ASSERT(t{:d}_{:d}=BVPLUS(1,q{:d}_{:d}_0,b{:d}_0,BVMULT(1,b{:d}_1,q{:d}_{:d}_1),BVMULT(1,b{:d}_2,BVMULT(1,q{:d}_{:d}_1,q{:d}_{:d}_2))));'.format(l,g,l,g,g,g,l,g,g,l,g,l,g))
            a=0
            for z in Z:
                print('ASSERT(x{:d}_{:s}=BVPLUS(1,BVMULT(1,a{:d}_{:d},t{:d}_{:d}),BVMULT(1,BVPLUS(1,a{:d}_{:d},0bin1),x{:d}_{:s})));'.format(g,z,g,a,l,g,g,a,g-1,z))
                a=a+1
             
                

        # S-box specific contraints
        # substitute the known pairs (x,y)
        binrepr = bin(l)[2:].zfill(n)
        for j in range(0, n):
            print(('ASSERT(x0_{:d}=0bin1);' if binrepr[j] == '1' else 'ASSERT(x0_{:d}=0bin0);').format(x))
            x = x + 1
        binrepr = bin(sbox[l])[2:].zfill(m)
        for j in range(0, m):
            print(('ASSERT(y_{:d}=0bin1);' if binrepr[j] == '1' else 'ASSERT(y_{:d}=0bin0);').format(y))
            y = y + 1

    for i in range(1,args.G+1):
        print('ASSERT(BVPLUS(2,0bin0@b{:d}_0,0bin0@b{:d}_1,0bin0@b{:d}_2)=0bin01);'.format(i,i,i))
        print('ASSERT(BVPLUS(3',end='')
        for j in range(0,n):
            print(',0bin00@a{:d}_{:d}'.format(i,j),end='')
        print(')=0bin001);')
        print('ASSERT(BVPLUS(3,0bin00@a{:d}_4,0bin00@a{:d}_5,0bin00@a{:d}_6,0bin00@a{:d}_7)=0bin001);'.format(i,i,i,i))
        print('ASSERT(BVPLUS(3,0bin00@a{:d}_8,0bin00@a{:d}_9,0bin00@a{:d}_10,0bin00@a{:d}_11)=0bin001);'.format(i,i,i,i))
        print('ASSERT(BVLE(BVPLUS(2,0bin0@a{:d}_0,0bin0@a{:d}_4,0bin0@a{:d}_8),0bin01));'.format(i,i,i))
        print('ASSERT(BVLE(BVPLUS(2,0bin0@a{:d}_1,0bin0@a{:d}_5,0bin0@a{:d}_9),0bin01));'.format(i,i,i))
        print('ASSERT(BVLE(BVPLUS(2,0bin0@a{:d}_2,0bin0@a{:d}_6,0bin0@a{:d}_10),0bin01));'.format(i,i,i))
        print('ASSERT(BVLE(BVPLUS(2,0bin0@a{:d}_3,0bin0@a{:d}_7,0bin0@a{:d}_11),0bin01));'.format(i,i,i))

    for i in range(0, len(sbox)):
        for j in range(0, 4):
            print(
                'ASSERT(y_{:d}=BVPLUS(1,BVMULT(1,k{:d}_0,x{:d}_{:d}),BVMULT(1,k{:d}_1,x{:d}_{:d}),BVMULT(1,k{:d}_2,x{:d}_{:d}),BVMULT(1,k{:d}_3,x{:d}_{:d})'
                '  ));'.format( i * 4 + j, j,args.G, i * 4, j, args.G,i * 4 + 1, j,args.G, i * 4 + 2, j, args.G,i * 4 + 3))

    for i in range(0, 4):
        print(
            'ASSERT(BVPLUS(3,0bin00@k{:d}_0,0bin00@k{:d}_1,0bin00@k{:d}_2,0bin00@k{:d}_3)=0bin001);'.format(i, i, i, i))
        print(
            'ASSERT(BVPLUS(3,0bin00@k0_{:d},0bin00@k1_{:d},0bin00@k2_{:d},0bin00@k3_{:d})=0bin001);'.format(i, i, i, i))
    
    print('T1,T2,T3:BITVECTOR(4);')
    print('T:BITVECTOR(8);')
    for l in range(0,3):
        print('ASSERT(T{:d}=BVPLUS(4'.format(l+1),end='')
        for i in range(1, args.G + 1):
            print(',0bin000@b{:d}_{:d}'.format(i,l),end='')
        print('));')
    print('ASSERT(T=BVPLUS(8,0bin0000@T1,0bin0000@T2,BVMULT(8,0bin0000@T3,0bin00000101)));')
    t=bin(args.T)[2:].zfill(8)
    print('ASSERT(BVLE(T,0bin{:s}));'.format(t))
    print('QUERY(FALSE);\nCOUNTEREXAMPLE;')
