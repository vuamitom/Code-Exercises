

# a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')


def score(s):
	# vowels are scored higher
	t = 0
	for i, c in enumerate(s):
		if c.lower() in ['a', 'e', 'i', 'o', 'u']:
			t += 3
		elif ord(c.lower()) > ord('a') and ord(c.lower()) < ord('z'):
			t += 1
		elif c == ' ' and i > 0 and i < len(s) - 1 and s[i - 1].isalpha() and s[i+1].isalpha():
			t += 1
	return t


def guess(a):
	# if True: return a 
	# if not len(a) == 60:
	# 	raise Exception('smth wrong, str len = ' + str(len(a)))

	b = [ord(c) for c in a]
	# b = [ord(c) for c in 'ETAOIN SHRDLU']
	r = ''
	s = 0
	for c in range(0, 256):
		o = [chr(i ^ c) for i in b]
		m = score(o)
		r = ''.join(o) if m > s else r 
		s = m if m > s else s
		# print ''.join(o) + ' score = ' + str(m) + ' char = ' + str(c)
	#print r 
	return (r, s)


# print guess('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex'))
# if True: 
# 	exit(0)
lines = None
with open('4.txt', 'r') as f:
	lines = f.readlines()
# print lines
for l in lines: 
	# print l
	v, s = guess(l.strip('\n').decode('hex'))
	if s >= 40:
		print v + ' score = ' + str(s)

