import time

spams = [
        "vay",
        "kho[aả]n vay",
        "vay v[oố]n",
        "vay ti[eề]n",
        "vay (?:t[ií]n|th[eế]) ch[aấ]p",
        "cho vay",
        "[uư]u [dđ][aã]i",
        "hỗ tr[oợ] v[oố]n",
        "gi[aả]i ng[aâ]n",
        "(?:cty|c[oô]ng ty) (?:t[aà]i ch[ií]nh|tc)",
        "(?:vay|v[oố]n|cvay) ti[eê]u d[uù]ng",
        "b[aả]o hi[eể]m nh[aâ]n th[oọ]",
        "th[eế] ch[aấ]p t[aà]i s[aả]n",
        "th[eẻ] t[ií]n d[uụ]ng",
        "l[aã]i su[aâấ]t|ls",
        "nv|(?:nh[aâ]n|chuy[eê]n) vi[eê]n",
        "t[uư] v[aấ]n",
        "ng[aâ]n h[aà]ng|nhnn",
        "điện thoại|s?[đd]t|tel\\b|telephone|call|liên (?:lạc|hệ)|\\blh\\b|gọi|contact|nhắn tin|(?:tin|lời) nhắn|sms"
    ]

non_capture_group = '|'.join(['(?:' + x + ')' for x in spams])
capture_group = '|'.join(['(' + x + ')' for x in spams])
noiter = 100

def get_input():
    content = None
    with open('/home/tamvm/Downloads/wikivietnam_token.txt', 'r') as f:
        content = f.readlines()
    return content

def get_long_input():
    pass

def test_python_re(lines):
    import re
    s = time.time()
    pattern = re.compile(non_capture_group)
    print('compiled in ', (time.time() - s) *1000, 'ms')
    s = time.time()
    for i in range(0, noiter):
        for l in lines:
            pattern.search(l)
    print('search with non capture group in ', (time.time() -s) *1000, 'ms')
    s = time.time()
    pattern = re.compile(capture_group)
    print('compiled in ', (time.time() - s) *1000, 'ms')
    s = time.time()
    for i in range(0, noiter):
        for l in lines:
            pattern.search(l)
    print('search with capturing group in ', (time.time() -s) *1000, 'ms')

    s = time.time()
    patterns = [re.compile(x) for x in spams]
    print('compiled in ', (time.time() - s) *1000, 'ms')
    s = time.time()
    for i in range(0, noiter):
        for l in lines:
            for p in patterns:
                p.search(l)
    print('run separate pattern in ', (time.time() -s) *1000, 'ms')

def test_python_re2(lines):
    pass
# test 
lines = get_input()
print('max sen len = ', max([len(l) for l in lines]))
print('>>>>>> python re:')
test_python_re(lines)

print('>>>>>> python google re2:')
test_python_re2(lines)
