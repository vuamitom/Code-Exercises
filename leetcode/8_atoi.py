class Solution(object):

    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        sign, start, end = None, None, None
        
        for i in range(0, len(s)):                        
            if start is None:
                if s[i] in ['-', '+'] and sign is None:
                    sign = -1 if s[i] == '-' else 1 
                elif s[i].isdigit():
                    start = i
                elif not s[i] == ' ' or sign is not None:
                    break 
            elif not s[i].isdigit():
                end = i
                break 
        if start is None:
            return 0
        if sign is None:
            sign = 1
        if end is None:
            end = len(s) 
        number = sign * int(s[start:end])        
        mx = 2**31
        if number < 0-mx:
            return 0-mx
        elif number > mx - 1:
            return mx -1 
        return number 

