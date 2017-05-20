import sys
import base64

def convert(ip):
    d = ip.decode('hex')
    return base64.b64encode(d)


ip = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'#sys.argv[1]

assert convert(ip) == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
