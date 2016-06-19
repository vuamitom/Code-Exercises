import sys
import binascii
from struct import *
"""
String input = "http://www.amazon.com/";
        Assert.assertEquals("7ac408c1dff9c84b", CacheUtil.getEntryHashKey(input));
        input = "http://www.domain.com/uoQ76Kb2QL5hzaVOSAKWeX0W9LfDLqphmRXpsfHN8tgF5lCsfTxlOVWY8vFwzhsRzoNYKhUIOTc5TnUlT0vpdQflPyk2nh7vurXOj60cDnkG3nsrXMhFCsPjhcZAic2jKpF9F9TYRYQwJo81IMi6gY01RK3ZcNl8WGfqcvoZ702UIdetvR7kiaqo1czwSJCMjRFdG6EgMzgXrwE8DYMz4fWqoa1F1c1qwTCBk3yOcmGTbxsPSJK5QRyNea9IFLrBTjfE7ZlN2vZiI7adcDYJef.htm";
        Assert.assertEquals("a68ac2ecc87dfd04", CacheUtil.getEntryHashKey(input));
        input = "http://stc3.ia.zdn.vn/js/jquery.1.0.1.js";
        Assert.assertEquals("d1102e599a66d517", CacheUtil.getEntryHashKey(input));
"""
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
    return ((payload_size, crc), memoryview(d)[offset + 8:])

def parse_index_meta(data):
    """
    long magicNo; --> uint64_t kSimpleIndexMagicNumber = UINT64_C(0x656e74657220796f);
    int version;
    long entryCount;
    long cacheSize;
    int reason;
    // Used in histograms. Please only add entries at the end.
      enum IndexWriteToDiskReason {
        INDEX_WRITE_REASON_SHUTDOWN = 0,
        INDEX_WRITE_REASON_STARTUP_MERGE = 1,
        INDEX_WRITE_REASON_IDLE = 2,
        INDEX_WRITE_REASON_ANDROID_STOPPED = 3,
        INDEX_WRITE_REASON_MAX = 4,
      };
    """
    bb = ByteBuffer(data)
    magic, version, entryCount, size, reason =  bb.readUInt8(), bb.readUInt4(), bb.readUInt8(), bb.readUInt8(), bb.readUInt4()
    # verify index meta
    print 'magic no: ' + str(magic)
    assert magic == 0x656e74657220796f
    print 'version: ' + str(version)
    # assert version == 7, 'index version out of date'
    # return data
    return magic, version, entryCount, size, reason

def parse_entries_meta(data, entry_count):
    entries = {}
    bb = ByteBuffer(data)
    print hex(unpack('Q', data[0:8].tobytes())[0])
    for i in xrange(0, entry_count): 
        # read key
        key = bb.readUInt8()
        if (key == 0xd1102e599a66d517): 
            print 'ALLKDJFLSKDJF LDSFJ'
        last_time = bb.readInt8()
        size = bb.readUInt8()
        entries[key] = (last_time, size)
    return entries
    

def parse_index_payload(data):
    """
    IndexMetadata + N * EntryMetadata
    EntryMetadata = key + hash + size
    """
    index_meta = parse_index_meta(data)
    _, _, entry_count, _, _ = index_meta
    entry_meta = parse_entries_meta(data[(8 + 4 + 8 + 8 + 4):], entry_count)
    return index_meta, entry_meta 

def read_index():
    file_name = sys.argv[1]
    r = None
    with open(file_name, 'rb') as f: 
        r = f.read()
    print 'Total file size = ' + str(len(r)) 
    header, payload = parse_pickle(r) 
    crc, size = header 
    verify_crc(crc, payload)
    print 'Payload size: ' + str(size)
    index_meta, entry_meta = parse_index_payload(payload)
    _, _, entryCount, size, reason = index_meta
    print 'Entry count: ' + str(entryCount) + ' Cache size: ' + str(size)
    total = 0

    print 'TOTAL = ' + str(total)


if __name__ == '__main__': 
    read_index()
