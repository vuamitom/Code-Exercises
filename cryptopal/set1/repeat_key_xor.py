import sys


def encrypt(a):
	# a = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
	k = 'ICE'
	o = []
	for i, c in enumerate(a):
		o.append(chr(ord(c) ^ ord(k[i % 3])))
	return ''.join(o).encode('hex')

f = sys.argv[1]
c = None
with open(f, 'r') as fp:
	c = fp.read()

print encrypt(c)