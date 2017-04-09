from heapq import *
from collections import deque

def solve(n, k):
	q = []
	heappush(q, (-n, -1, -(n+2)))
	t = k
	while t > 0:
		tt = heappop(q)
		
		d, s, e = tt
		d = 0 - d
		s = 0 - s
		e = 0 - e
		# print (s, e, d)
		# look for place to insert 
		p = s + (e - s)/2
		l = p - s - 1
		r = e - p - 1
		heappush(q, ( - l, -s, -p))
		heappush(q, ( - r, -p, - e))
		if t == 1:
			return (max(l, r), min(l, r))		
		t -= 1	

# def solve3(n, k):
# 	q = deque()
# 	q.append((1, n+2))
# 	t = k
# 	while t > 0:
# 		# print str(list(q))
# 		s, e = q.popleft()		
# 		print (s, e, e - s - 1)		
# 		# look for place to insert 
# 		p = s + (e - s)/2
# 		l = p - s - 1
# 		r = e - p - 1
# 		if l >= r: 			
# 			q.append((s, p))
# 			q.append((p, e))
# 		elif l < r:
# 			q.append((p, e))
# 			q.append((s, p))	
			
# 		if t == 1:
# 			f = (max(l, r), min(l, r))		
# 			print f
# 			return f
# 		t -= 1
		

def solve2(n, k):	
	# print (n, k)
	l = (n - 1)/2
	r = n/2
	if k == 1:
		# print 'aaaa'
		return (r, l)
	if l == 0 and r == 0: 
		# print 'aaa1'
		return (0, 0)
	elif l == 0:
		return solve2(r, k)
	elif r == 0:
		return solve2(l, k)

	k -= 1
	if k % 2 == 0:
		# print 'a1'
		return solve2(l, k/2)
	elif l == r:
		# print 'a2'
		return solve2(r, k/2 + 1)
	else:		
		return solve2(r, k/2 + 1)
		# t2 = solve2(r, k/2)		
		


def test(func):
	assert func(4, 2) == (1, 0)
	assert func(5, 2) == (1, 0)
	assert func(6, 2) == (1, 1)
	assert func(1000, 1000) == (0, 0)
	assert func(1000, 1) == (500, 499)
	assert func(1000, 2) == (250, 249)
	assert func(3, 1) == (1, 1)
	assert func(3, 2) == (0, 0)
	assert func(2, 1) == (1, 0)
	assert func(2, 2) == (0, 0)

def test2(func):
	# assert func(500000, 249999) == (1, 0)
	assert solve(999, 498) == solve2(999, 498)
	assert solve(999, 497) == solve2(999, 497)
	# assert solve(606, 578) == solve3(606, 578)
	assert func(1000, 999) == (0, 0)
	assert func(500000, 499999) == (0, 0)
# print '------'
# print solve(999, 498)
# print solve2(999, 498)
assert solve(62, 30) == solve2(62, 30)
assert solve(6, 3) == solve2(6, 3)
assert solve(30, 15) == solve2(30, 15)

# print solve(62, 31)
# print solve2(30, 15)
# print '------'
# test(solve2)	
# test2(solve2)
# solve(606, 578)

# test()
t = int(raw_input()) 
for i in xrange(1, t + 1):
    n, k = [int(x) for x in raw_input().split(" ")]       
    l, r = solve2(n, k)
    print 'Case #' + str(i) + ': ' + str(l) + ' ' + str(r)