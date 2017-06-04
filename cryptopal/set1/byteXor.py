

# a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')
freq = {
	'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015,
	'h': 6.094, 'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406,
	'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 
	't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974, 'z': 0.074
}

board = {}
alp = sorted([x for x in range(ord('a'), ord('z') + 1)], key = lambda x: freq[chr(x)])
for i, c in enumerate(alp): 
	board[chr(c)] = i + 1
# print ' score board = ' + str(board)

def score(s, log = False):
	# vowels are scored higher
	t = 0
	histogram = {}
	for i, c in enumerate(s):
		a = c.lower()
		# if ord(a) >= ord('a') and ord(a) <= ord('z'):
		# 	if a not in histogram:
		# 		histogram[a] = 1
		# 	else:
		# 		histogram[a] += 1
		if a in board:
			t += board[a]

		# if c.lower() in ['a', 'e', 'i', 'o', 'u']:
		# 	t += 3
		# elif ord(c.lower()) > ord('a') and ord(c.lower()) < ord('z'):
		# 	t += 1
		elif c == ' ' and i > 0 and i < len(s) - 1 and s[i - 1].isalpha() and s[i+1].isalpha():
			t += 1
	# for k in histogram:
	# 	f = histogram[k] * 100.0 / len(s)
	# 	histogram[k] = f
	# 	e = freq[k]
	# 	t += 1 - abs(f - e) / e
	# if log:
	# 	print histogram
	return t


def guess(a, log = False):
	# if True: return a 
	# if not len(a) == 60:
	# 	raise Exception('smth wrong, str len = ' + str(len(a)))

	b = [ord(c) for c in a]
	# b = [ord(c) for c in 'ETAOIN SHRDLU']
	r = ''
	s = 0
	k = None
	for c in range(0, 256):
		o = [chr(i ^ c) for i in b]
		m = score(o, c == 53)
		r = ''.join(o) if m > s else r 
		k = c if m > s else k
		s = m if m > s else s
		# if log and c < 31:
			# print ''.join(o) + ' score = ' + str(m) + ' char = ' + str(c)
	 
	return (r, s, k)


# print guess('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex'))
# if True: 
# 	exit(0)
if __name__ == '__main__':
	lines = None
	with open('4.txt', 'r') as f:
		lines = f.readlines()
	# print lines
	v, s, k = guess(lines[170].strip('\n').decode('hex'))
	print v + ' score = ' + str(s) + ' key = ' + str(k) + ' line = '	

	# for ix, l in enumerate(lines): 
	# 	# print l
	# 	v, s, k = guess(l.strip('\n').decode('hex'))
		# if s >= 41:
		# 	print v + ' score = ' + str(s) + ' key = ' + str(k) + ' line = ' + str(ix)

