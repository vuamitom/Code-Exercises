
def fn1():
	import math
	import numpy as np
	res = []
	for x in range(0, 10):
		res.append(math.floor(2000 - 10 * x * 	(np.exp(5 - x**2/8))))

	print(res)

def fn2():
	fac = 1
	x = 5
	s = 1
	for j in range (1, 1000):
		s = s + (x ** j)/ (fac * 1.0)

		fac = fac * (j+1)
		print(' s= ' +str(s) + ' fac = ' + str(fac)	)
	print ('sum = ' + str(s))

def fn3():
	e = 1
	c = 0
	for m in range (0, 13):
		le = e
		e = c
		c = c + le
		print ('End of month ' + str(m + 1) + ' egg = ' + str(e) + ' chick = ' + str(c))

def find_room(M):
	mp = -1
	s = [(0, 0), (1, 0), (0, 1), (1, 1)]
	for r in range(0, len(M) - 1):
		for c in range (0, len(M[0]) - 1):
			p = sum ([M[r+x][c+y] for (x, y) in s])
			mp = p if p > mp else mp
	return mp

from random import randint
def guess_number(low, high, random=True):
	if (low > high):
		raise ValueError('Cheater!')
	if random:
		return randint(low, high)
	else:
		return int(low + (high - low) / 2)

def game():
	l, h = 0, 1000
	for t in range (0, 10):
		n = guess_number(l, h, t == 0)
		print(n)
		user = input('Is it correct?: ').upper()
		if user not in ('E', 'L', 'G'):
			raise ValueError('Input must be either E, L or G')
		if user == 'E':
			print('machine won!')
			return
		elif user == 'G':
			l = n + 1
		elif user == 'L':
			h = n - 1
	print('machine lost!')


			
import numpy as np
def rot90cw(x):
	return np.flip(x.transpose(), 1)


def update_avg(last_avg, last_count, new_input):
	return (last_avg * last_count + new_input) / (last_count + 1)

import random
def pick_article(scores):
	s = sum(scores)
	dist = [x / s for x in scores]
	r = random.uniform(0, 1)
	t = 0
	for i in range(0, len(dist)):
		t += dist[i]
		if (t >= r):
			return (i + 1)
	return len(dist)


def is_perfect(n):
	d = []
	for x in range(1, n):
		if (n % x == 0):
			d.append(x)
	return n == sum(d)

for d in [6, 10,  28, 100, 496, 8128]:
	print(str(d) + ' is perf = ' + str(is_perfect(d)))