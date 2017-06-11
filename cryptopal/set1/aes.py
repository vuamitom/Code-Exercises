from Crypto.Cipher import AES
import base64

obj = AES.new("YELLOW SUBMARINE", AES.MODE_ECB, "0" * 16)
content = None
with open('7.txt', 'r') as f:
	content = f.read()


print obj.decrypt(base64.b64decode(content)[0:16])