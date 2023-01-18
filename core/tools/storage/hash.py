"""
@prere: pip install hashlib 
@Desc: This function returns the SHA-1 hash of the file passed into it
@param: paths: path, File path
@output: hash: hash,  

"""

import os
import os.path as op
import hashlib

def getHash(path): 
    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(path,'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
    # return the hex representation of digest
    return h.hexdigest()