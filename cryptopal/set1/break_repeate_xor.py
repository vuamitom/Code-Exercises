import base64
import byteXor

def hamming_distance(a, b):	
	x = [ord(c) for c in a]
	y = [ord(c) for c in b]
	l = min(len(x), len(y))
	d = 0
	for i in range(0, l):
		r = x[i] ^ y[i]
		for j in range(0, 8):
			d += (r >> j) & 0x01 # otherwise, use technique to detect 1bit : val& (val -1)
	# print 'd = ' + str(d)
	return d

def guess_key_length(ip):
	m = 99999
	keysize = 0

	for s in range(2, 41):
		w1 = ip[0:s]
		w2 = ip[s:2*s]
		d = hamming_distance(w1, w2)/s
		if d < m:
			m = d
			keysize = s
	print 'min hamming_distance = ' + str(m)
	return keysize

def solve(inp):
	keysize = guess_key_length(inp)
	bl = [[]] * keysize
	key = []
	for i, c in enumerate(inp):
		bl[i % keysize].append(c)
	for b in bl:
		v, s, k = byteXor.guess(b)
		key.append(k)
	return key

def decryptXOR(inp, key):
	o = []
	for i, c in enumerate(inp):
		o.append(ord(c) ^ key[i % len(key)])
	return ''.join(chr(c) for c in o)


# print hamming_distance('t', 'w')
assert hamming_distance('this is a test', 'wokka wokka!!!') == 37
inp = None
with open('6.txt', 'r') as f:
	inp = f.read()

inp = base64.b64decode(inp)
key = solve(inp)
print decryptXOR(inp, key)