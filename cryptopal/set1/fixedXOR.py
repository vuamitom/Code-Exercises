a = '1c0111001f010100061a024b53535009181c'
b = '686974207468652062756c6c277320657965'

a2 = [ord(c) for c in a.decode('hex')]
b2 = [ord(c) for c in b.decode('hex')]
o = []
for i in range(0, len(a2)):
    o.append(a2[i] ^ b2[i])
print (''.join(chr(c) for c  in o)).encode('hex')
