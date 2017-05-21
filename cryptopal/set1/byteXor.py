

a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')
b = [ord(c) for c in a]
r = ''
s = 0

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



for c in range(0, 256):
	o = [chr(i ^ c) for i in b]
	m = score(o)
	r = ''.join(o) if m > s else r 
	s = m if m > s else s
	# print ''.join(o) + ' score = ' + str(m)
print r 

