import sys
import base64

def h2d(c):
	m = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
	if c in m: 
		return m[c]
	return int(c)

def hex2str(ip):
	b = []
	for c in range(0, len(ip)):
		if c % 2 == 0:
			b.append(h2d(ip[c]) * 16  + h2d(ip[c + 1]))
	return b
	# return ''.join([chr(c) for c in b])

b64index = []
for i in range(ord('A'), ord('Z') + 1):
	b64index.append(chr(i))
for i in range(ord('a'), ord('z') + 1):
	b64index.append(chr(i))
for i in range(ord('0'), ord('9') + 1):
	b64index.append(chr(i))

b64index.append('+')
b64index.append('/')


def b64e(ip):
	b = []
	for c in range(0, len(ip), 3):					
		for i in range(c, c + 3):			
			if i % 3 == 0:
				b.append((ip[i] & 0xFC) >> 2)
				if i == len(ip) - 1:
					b.append((ip[i] & 0x03) << 4)
					break

			elif i % 3 == 1:
				b.append(((ip[i - 1] & 0x03) << 4) | ((ip[i] & 0xf0) >> 4))
				if i == len(ip) - 1:
					b.append((ip[i] & 0x0f) << 2)
					break
			else:
				b.append(((ip[i - 1] & 0x0f) << 2) | ((ip[i] & 0xc0) >> 6))			
				b.append(ip[i] & 0x3f)

	print b
	r = ''.join([b64index[c] for c in b])
	if len(ip) % 3 == 2:
		r += '='
	elif len(ip) %3 == 1:
		r += '=='
	return r


def convert(ip):
    d = ip.decode('hex')
    return base64.b64encode(d)

ip = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'#sys.argv[1]


s = hex2str(ip)
# print s 
print ''.join([chr(c) for c in s])
print b64e(s[0:4])
assert b64e(s) == convert(ip)
assert convert(ip) == 'SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t'
