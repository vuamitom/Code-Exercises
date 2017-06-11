from Crypto.Cipher import AES
import base64


IV = chr(0x00) * 16
key = 'YELLOW SUBMARINE'

obj = AES.new(key, AES.MODE_ECB, "0" * 16)

c = None
with open('10.txt', 'r') as f: 
	c = f.read()


def encrypt(inp):
	out = [IV]
	for i in range(0, len(inp), 16):
		b = inp[i: (i + 16)]
		p = out[len(out) - 1]
		y = block_xor(b, p)
		c = obj.encrypt(y)
		out.append(c)
	return out[1:]

def decrypt(inp):
	out = []
	for i in range(0, len(inp), 16):
		b = inp[i: (i + 16)]
		c = obj.decrypt(b)
		p = IV if i == 0 else inp[(i - 16):i]
		out.append(block_xor(c, p))
	return out



def block_xor(a2, b2):
	o = []
	for i in range(0, len(a2)):
	    o.append(ord(a2[i]) ^ ord(b2[i]))
	return ''.join(chr(c) for c  in o)

print ''.join(decrypt(base64.b64decode(c)))