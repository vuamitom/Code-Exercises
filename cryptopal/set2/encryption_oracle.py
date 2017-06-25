import random
from Crypto.Cipher import AES
import pkcs7_padding


def ecb(inp, k):
	obj = AES.new(k, AES.MODE_ECB, gen_aes_key())
	# print 'original = ' + repr(obj.encrypt(ori))
	return obj.encrypt(pkcs7_padding.pad(inp, 16))

def cbc(inp, k):
	obj = AES.new(k, AES.MODE_CBC, gen_aes_key())
	
	return obj.encrypt(pkcs7_padding.pad(inp, 16))

def gen_aes_key():
	return ''.join([chr(x) for x in random.sample(xrange(256), 16)])

def gen_text():
	c = random.randint(5, 10)
	return ''.join([chr(x) for x in random.sample(xrange(256), c)])	

def encrypt(inp):
	k = gen_aes_key()
	pl = gen_text() + inp + gen_text() 
	# pl = inp
	t = random.randint(0, 1) 
	if t == 0:
		# print 'ecb -'
		return (ecb(pl, k), 0)
	else:
		# print 'cbc -'
		return (cbc(pl, k), 1)


def detect(en, d = False):
	# if d:
	# 	print repr(en)
	for i, _ in enumerate(en):
		if i + 16 < len(en):
			if en[i] == en[i + 16]:
				ecb = True
				for j in range(1, 16):
					if not en[i + j] == en[i + j + 16]:
						ecb = False
						break
				if ecb:
					return 0
	return 1

def encrypt_oracle(inp):
	for i in range(0, 10):
		r, t = encrypt(inp)
		gt = detect(r, t == 0)
		assert gt == t
		print ('ECB' if gt == 0 else 'CBC')



# encrypt_oracle('YELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINEYELLOW SUBMARINE')		
