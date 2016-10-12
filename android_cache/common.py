# common
from struct import *
import binascii

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

    def readUInt2(self): 
        r = unpack_from('<H', self.data, self.offset)
        self.offset += 2
        return r[0]


    def readData(self):
        dlen = self.readUInt4()
        
        r = dlen, self.data[self.offset:(self.offset + dlen)]
        self.offset += dlen 
        return r

    def readString(self):
        slen = self.readUInt4()
        r = self.data[self.offset: (self.offset + slen)]
        self.offset += slen
        return slen +  (4- slen % 4) % 4, r
        # return slen, r

    def data(self):
        return self.data

    def offset(self):
        return self.offset

def verify_crc(crc, data):
    real_crc = binascii.crc32(data)
    assert real_crc == crc

def parse_pickle(d, offset = 0): 
    """
    Pickle (PickleHeader + Payload)
    PickleHeader = CRC (4bytes) + PayloadSize (4bytes)
    """
    bb = ByteBuffer(d, offset)
    crc = bb.readUInt4()
    payload_size = bb.readUInt4()
    return ((payload_size, crc), d[offset + 8:])

