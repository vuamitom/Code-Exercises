import sys
from common import *
from response_info import *
import m509
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
SIMPLE_EOF_SIZE = 8 + 4 + 4 + 4 + 4 # for some reason, there are last 5 bytes which I don't know what's for
SIMPLE_HEADER = 8 + 4 * 3
SIMPLE_FINAL_MAGICNO = 0xf4fa6f45970d41d8
SIMPLE_INI_MAGICNO = 0xfcfb6d1ba7725c30

FLAG_HAS_CRC32 = 1 << 0
FLAG_HAS_SHA256 = 1 << 1

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
    s0_eof = read_simple_eof(data[-SIMPLE_EOF_SIZE:])
    magic, flag, crc, ssize = s0_eof 
    s0_eof_offset = SIMPLE_EOF_SIZE
    assert magic == SIMPLE_FINAL_MAGICNO, 'Magic no. not match SimpleFinalMagicNo' 
    if flag & FLAG_HAS_CRC32:
        # verify crc 
        # print crc
        pass 
    if flag & FLAG_HAS_SHA256:
        s0_eof_offset += 32

    stream0 = data[-(s0_eof_offset + ssize): - s0_eof_offset]
    s1_eof = read_simple_eof(data[-(s0_eof_offset + ssize + SIMPLE_EOF_SIZE): -(s0_eof_offset+ssize)])
    magic1, flag1, crc1, ssize1 = s1_eof

    assert magic1 == SIMPLE_FINAL_MAGICNO
    
    stream1 = data[-(s0_eof_offset + ssize + SIMPLE_EOF_SIZE + ssize1): -(s0_eof_offset + ssize + SIMPLE_EOF_SIZE)]
    key = data[SIMPLE_HEADER:-(s0_eof_offset + ssize + SIMPLE_EOF_SIZE + ssize1)]
    file_header = read_simple_file_header(data[0:SIMPLE_HEADER])
    hmagic, hversion, hkeylen, hkeyhash = file_header

    assert hmagic == SIMPLE_INI_MAGICNO

    print 'Key = ' + key.tobytes()
    print 'Stream0 size = ' + str(ssize)
    parse_response_info(stream0)
    print stream0.tobytes()
    print 'Stream1 size = ' + str(ssize1)
   
    return None, None, None

def parse_response_headers(data):
    # pass raw 
    current = 0
    status = None
    for i, c in enumerate(data):
        if c =='\0':
            status = data[0:i].tobytes()
            current = i
            break
    print status

    return data[i:].tobytes().split('\0') 


def parse_response_info(data):
    phead, payload = parse_pickle(data)
    # verify crc 
    payload_size, crc = phead
    # verify_crc(crc, payload)
    bb = ByteBuffer(payload)
    flags = bb.readUInt4()
    version = flags & RESPONSE_INFO_VERSION_MASK
    assert version < RESPONSE_INFO_MINIMUM_VERSION or version > RESPONSE_INFO_VERSION, 'Unexpected response info version'
    data = payload
    req_time = bb.readUInt8()
    res_time = bb.readUInt8()
    # read header 
    # probably we have picked the wrong start of stream0
    # byright, offset should've been 4 + 16
    remain = data[( 16):]
    bb = ByteBuffer(remain)
    slen, header_data = bb.readString()
    print ' str len = ' + str(slen)

    headers = parse_response_headers(header_data)

    # again, for some reason i don't know 
    # offset += 4
    remain = remain[(slen + 4):]
    print '\n'.join(headers)
    if flags & RESPONSE_INFO_HAS_CERT:
        cl, cert = m509.read_cert(remain) 
        if cert is not None:
            print cert.get_issuer()
            print cert.get_subject()
        remain = remain[cl:]

    if flags & RESPONSE_INFO_HAS_CERT_STATUS: 
        print 'cert_status: '
        # cert_status = None
        remain = remain[4:]
    # vary-data 
    if flags & RESPONSE_INFO_HAS_VARY_DATA:
        vary_data = remain[0:16]
        remain = remain[16:]

    print [hex(ord(c)) for c in remain[20:40]]
    print remain.tobytes()
    # socket-address
    bb = ByteBuffer(remain)
    hl, host = bb.readString()
    print str(hl)
    print host
    port = bb.readUInt2()

    print 'host = ' + host + ':' + str(port)


    # protocol version 

    # connection info 

    # key_exchange_info 

    #
        

     
if __name__ == '__main__':

    f = sys.argv[1]
    c = None
    with open(f, 'rb') as fi:
        c = fi.read()
    data = memoryview(c)
    # print 'Total file size = ' + str(len(c))
    # pickle_header, payload = parse_pickle(data)
    # crc, size = pickle_header
    # print 'Payload size = ' + str(size)
    # verify_crc(crc, payload)
    header, s1, s0 = read_stream01(data)
