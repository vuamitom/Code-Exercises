class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """
        vals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000, 'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
        i, v = 0, 0        
        while i < len(s):
            if i < len(s) - 1 and s[i:i+2] in vals: 
                v += vals[s[i:i+2]]
                i += 2 
            else:
                v += vals[s[i]]
                i += 1
        return v 


        
