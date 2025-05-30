def isPlaindrome(s):
    return ''.join(reversed(s)) == s 

def palindromeIndex(s):
    # Write your code here
    if isPlaindrome(s):
        return -1 
    for idx, _ in enumerate(s):
        test = s[0:idx] + s[(idx + 1):]
        # print('>>>', test, isPlaindrome(test))
        if isPlaindrome(test):
            return idx 
    return -1

print(palindromeIndex('aaab'))
print(palindromeIndex('aaa'))
print(palindromeIndex('a'))
print(palindromeIndex('ab'))
print(palindromeIndex('aa'))
print(palindromeIndex('abca'))
print(palindromeIndex('abcda'))
print(palindromeIndex('abccba'))
print(palindromeIndex('axxxxxxxx'))
print(palindromeIndex('x'))
