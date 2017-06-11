
c = None
with open ('8.txt', 'r') as f: 
	c = f.read()

ls = []
for l in c.split('\n'):
	ls.append(l.decode('hex')) 
# print ls
ls = ls[0:(len(ls) - 1)]
blocks = {}
possible_line = None
for r, l in enumerate(ls):
	b = None
	for i, c in enumerate(l):
		if i% 16 == 0:
			if b:
				k = ''.join(b)
				if k in blocks:
					print 'DUP!!! in line ' + str(r)
					possible_line = r
				blocks[k] = True
			b = []
		b.append(c)
# print blocks
if possible_line:
	print ls[possible_line]