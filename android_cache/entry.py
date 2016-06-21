import sys
from common import ByteBuffer
"""
 // A file containing stream 0 and stream 1 in the Simple cache consists of:
 //   - a SimpleFileHeader.
 //   - the key.
 //   - the data from stream 1.
 //   - a SimpleFileEOF record for stream 1.
 //   - the data from stream 0.
 //   - (optionally) the SHA256 of the key.
 //   - a SimpleFileEOF record for stream 0.
 //
 // Because stream 0 data (typically HTTP headers) is on the critical path of
 // requests, on open, the cache reads the end of the record and does not
 // read the SimpleFileHeader. If the key can be validated with a SHA256, then
 // the stream 0 data can be returned to the caller without reading the
 // SimpleFileHeader. If the key SHA256 is not present, then the cache must
 // read the SimpleFileHeader to confirm key equality.

 // A file containing stream 2 in the Simple cache consists of:
 //   - a SimpleFileHeader.
 //   - the key.
 //   - the data.
 //   - at the end, a SimpleFileEOF record.
"""
SIMPLE_EOF_SIZE = 8 + 4 + 4 + 4
SIMPLE_HEADER = 8 + 4 * 3
SIMPLE_FINAL_MAGICNO = 0xf4fa6f45970d41d8

def read_simple_file_header(data):
    """
            uint64_t initial_magic_number;
            uint32_t version;
            uint32_t key_length;
            uint32_t key_hash;
    """
    bb = ByteBuffer(data)
    return bb.readUInt8(), bb.readUInt4(), bb.readUInt4(), bb.readUInt4()

def read_simple_eof(data):
    """
    struct NET_EXPORT_PRIVATE SimpleFileEOF {
      enum Flags {
        FLAG_HAS_CRC32 = (1U << 0),
        FLAG_HAS_KEY_SHA256 = (1U << 1),  // Preceding the record if present.
      };
    
      SimpleFileEOF();
    
      uint64_t final_magic_number;
      uint32_t flags;
      uint32_t data_crc32;
      // |stream_size| is only used in the EOF record for stream 0.
      uint32_t stream_size;
    };
    """
    bb = ByteBuffer(data)
    return bb.readUInt8(), bb.readUInt4(), bb.readUInt4(), bb.readUInt4()
     

def read_stream01(data):
    # header = read_simple_file_header(data)
    # read s0 eof 
    s0_eof = read_simple_eof(data[- SIMPLE_EOF_SIZE:])
    magic, flag, crc, ssize = s0_eof 
    assert magic == SIMPLE_FINAL_MAGICNO
    return None, None, None

     
if __name__ == '__main__':

    f = sys.argv[1]
    c = None
    with open(f, 'rb') as fi:
        c = fi.read()

    header, s1, s0 = read_stream01(memoryview(c))
