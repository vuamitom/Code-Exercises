from M2Crypto import X509
from common import *
import tempfile

def cert_from_bytes(data):
    f = tempfile.mkstemp()
    with open(f[1], 'wb') as fi:
        fi.write(data.tobytes())
    cptr = X509.load_cert(f[1], X509.FORMAT_DER)
    return cptr

def read_cert(data):
    # read length 
    bb = ByteBuffer(data)
    chain_len = bb.readUInt4()
    cert_chain = []
    # read data
    total = 4
    for i in range(0, chain_len):
        dl, dd = bb.readData()
        if not dl > 0: 
            return None
        cert_chain.append(dd)
        total += 4 + dl 
    if len(cert_chain) == 0: 
        return None 

    intermediate_certs = []
    for cert in cert_chain[1:]:
        intermediate_certs.append(cert_from_bytes(cert)) 
    handle = None 
    if len(intermediate_certs) == len(cert_chain)-1:
        handle =  cert_from_bytes(cert_chain[0])

    # if handle is not None: 
    #     # create cert 
    #     return None
    return total, handle
   
