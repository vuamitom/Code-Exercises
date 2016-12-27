n = raw_input()
l = raw_input()
l = [int(x) for x in l.split(' ')]
l.sort()
no = False
for i, x in enumerate(l):
    if i < len(l) - 1 and not x == l[i+1] and x*2 > l[i+1]:
        no = True
        break
print ('YES' if no else 'NO')
