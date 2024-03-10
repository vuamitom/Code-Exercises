# https://leetcode.com/problems/longest-palindromic-substring/
class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        mxpl = 0
        prev = None
        palin = None
        for i in range (0, len(s)):
            p = [(1, s[i])]    
            if prev is not None:
                for l, c in prev: 
                    if c is not None and c == s[i]:
                        p.append(((l + 1), c))
                    elif i - l -1 >= 0 and s[i] == s[i - l - 1]:
                        p.append(((l + 2), None))
            for l, _ in p: 
                if l > mxpl:
                    mxpl = l 
                    palin = (i + 1 - l, i+1)
            prev = p
        return s[palin[0]:palin[1]]
    
                
        
                
        