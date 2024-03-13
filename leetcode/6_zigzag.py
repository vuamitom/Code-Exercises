# https://leetcode.com/problems/zigzag-conversion/
class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows == 1:
            return s             
        r = []
        for i in range(0, numRows):
            upGap = (numRows - i - 1)  * 2
            downGap = (i - 0) * 2 
            j = i
            c = 0
            while j < len(s):
                r.append(s[j])
                j += upGap if (c % 2 == 0 and upGap > 0) or downGap == 0 else downGap 
                c += 1                 
        return ''.join(r)
