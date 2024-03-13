class Solution(object):
    def toDigits(self, x, base):
        r = []
        while x > 0:
            r.append(x % base)
            x = x / base 
        return r 
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        r = self.toDigits(abs(x), 10)
        n = 0
        m = 1
        for i in range(0, len(r)):
            n += m * r[len(r) - i - 1]
            m = m * 10 
        binary = self.toDigits(n, 2)
        sign = 1 if x >= 0 else -1
        if len(binary) <= 31:
            return n * sign
        elif len(binary) == 32:
            return n * sign if x < 0 and sum(binary[0:-1]) == 0 else 0 
        else:
            return 0
            