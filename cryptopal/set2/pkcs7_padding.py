

def pad(inp, bl):
	c = len(inp) % bl
	if not c == 0:
		c = bl - c
	# print (chr(c) * c)
	return inp + (chr(c) * c)

# print repr(pad('YELLOW SUBMARINE', 20))