import os

p = '/home/tamvm/Downloads/wikivietnam.txt'
with open(p, 'r') as f:
    content = f.read()
content = [c.strip() for c in content.split('\n') if c]
lines = []
for c in content:
    if c:
        sen = [x.strip() for x in c.split('.') if x]
        if len(sen) > 0:
            lines += sen
print(lines)
print(len(lines))

with open('/home/tamvm/Downloads/wikivietnam_token.txt', 'w') as f:
    f.write('\n'.join(lines))