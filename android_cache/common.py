# common
from struct import *

class ByteBuffer(object):
    
    def __init__(self, data, init_offset = 0): 
        self.data = data
        self.offset = init_offset 

    def readUInt4(self):
        r = unpack_from('<I', self.data, self.offset)
        self.offset += 4
        return r[0]

    def readUInt8(self):
        r = unpack_from('<Q', self.data, self.offset)
        self.offset += 8
        return r[0]

    def readInt8(self): 
        r = unpack_from('<q', self.data, self.offset)
        self.offset += 8
        return r[0]
        

    def data(self):
        return self.data

    def offset(self):
        return self.offset
