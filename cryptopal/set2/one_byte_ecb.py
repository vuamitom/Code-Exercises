import encryption_oracle
import base64
from Crypto.Cipher import AES
import pkcs7_padding

key = encryption_oracle.gen_aes_key()

extra = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")




# def ecb(inp, k):
# 	obj = AES.new(k, AES.MODE_ECB, gen_aes_key())
# 	# print 'original = ' + repr(obj.encrypt(ori))
# 	return obj.encrypt(pkcs7_padding.pad(inp, 16))

def aes_128_ecb(inp):
	txt = inp + extra
	e = encryption_oracle.ecb(txt, key)
	return e

def find_identical_substr(s1, s2):
	c = 0
	for i in range(0, len(s1)):
		if s1[i] == s2[i]:
			c += 1
		else:
			return c
	return c

def detect_block_size():
	prev = None
	for x in xrange(1, 32):
		t = 'A' * x
		ent = aes_128_ecb(t)
		if prev:
			l = find_identical_substr(ent, prev)
			if l > 0:
				return l
		prev = ent
		# print t
		# print t + ' --> ' + repr(ent)
	return -1

def is_ecb(bs):
	s = 'A' * bs
	s = s + s + s 
	return encryption_oracle.detect(aes_128_ecb(s)) == 0

def nothing(bs):
	s = 'A' * (bs - 1)
	ent = aes_128_ecb(s)
	b1 = ent[0:bs]
	# detect fill in byte 
	for x in xrange(0, 256):
		s = 'A' * (bs - 1) + chr(x)
		ent = aes_128_ecb(s)
		b2 = ent[0:bs]
		if b1 == b2:
			print 'found last byte =  ' + str(chr(x))

	# print s + ' ---> ' + repr(ent)
	# s = 'A' * (bs)
	# ent = aes_128_ecb(s)
	# print s + ' ---> ' + repr(ent)

bs = detect_block_size()
print 'block size = ' + str(bs)
print 'is_ecb = ' + str(is_ecb(bs))
nothing(bs)