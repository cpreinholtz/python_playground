#!/usr/bin/env python
import pathlib
import zipfile
import os
import numpy.distutils.exec_command as npe


def main():
    pts = "C:\\Users\\clark\\Desktop\\kindletest\\kindletest"
    pt = pathlib.Path(pts)
    print("testing rar organizer")
    #print(pt.glob('*'))
    for aut in pt.glob('*'):
        print()
        print(aut.__str__().split(pts)[1])
        for book in aut.glob('*'):
            print(book.__str__().split(aut.__str__())[1])




def mainold():


    pt = pathlib.Path("C:\\Users\\clark\\Desktop\\kindletest2")
    print("testing rar organizer")
    print(pt)

    cmd ="rar x {}\\*".format(pt.__str__())
    print(cmd)

    rardir = pathlib.Path("C:\\Program Files\\WinRAR\\")
    print(rardir)
    ret = npe.exec_command(cmd, execute_in=rardir)
    print(ret)
    '''

    for f in pt.glob("*op.rar"):
        print()
        print(f)
        print(f.__str__().split())


        cmd ="rar x '{}'".format(f)
        print(cmd)
        di = pathlib.Path("C:\\Program Files\\WinRAR\\")
        print(di)
        ret = npe.exec_command(cmd, execute_in=di)
        print(ret)
        #zf = zipfile.ZipFile(f)
        #print(zf.namelist())
        '''




if __name__ == '__main__':
    main()
