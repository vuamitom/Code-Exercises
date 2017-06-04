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
	al = []
	for s in range(2, 41):
		w1 = ip[0:s]
		w2 = ip[s:2*s]
		d = hamming_distance(w1, w2)/ (s * 1.0)
		al.append((s, d))
		if d < m:
			m = d
			keysize = s
	al =  sorted(al, key= lambda x: x[1])
	print 'min hamming_distance = ' + str(m)
	return al[15:20]

def solve(inp):
	keysizes = guess_key_length(inp)
	for ks in keysizes:#range(1, 5):
		keysize = ks[0]
		# print ' key_size = ' + str(keysize)
		bl = [[] for i in range(0, keysize)]
		# print ' initial = ' + str(bl) + ' inp len = ' + str(len(inp))
		key = []
		# test = {0: 0, 1:0, 2:0, 3: 0, 4:0}
		for i, c in enumerate(inp):
			# print 'b no = ' + str(i % keysize)
			# test[i % keysize] += 1
			bl[i % keysize].append(c)
		# print 'test = ' + str(test)
		# print ' all size = ' + str([len(b) for b in bl])
		log = True
		for b in bl:
			# print 'block len = ' + str(len(b))
			v, s, k = byteXor.guess(b, log)
			log = False
			# print 'score = ' + str(s) + ' key = ' + str(k) + ' ' + v
			# print ' val  = ' + v

			key.append(k)
		print 'key = ' + str(key)
		r = decryptXOR(inp, key)
		print r 
		# break

def decryptXOR(inp, key):
	o = []
	for i, c in enumerate(inp):
		o.append(ord(c) ^ key[i % len(key)])
	return ''.join(chr(c) for c in o)


# print hamming_distance('t', 'w')
x = hamming_distance('this is a test', 'wokka wokka!!!')
assert  x == 37
print 'normalize dist = ' + str(x * 1.0 / len('this is a test'))
inp = None
with open('6.txt', 'r') as f:
	inp = f.read()

inp = base64.b64decode(inp)
key = solve(inp)
# print decryptXOR(inp, key)