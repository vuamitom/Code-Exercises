class Solution(object):
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        o, c = 8, 8
        res = []
        for _ in range(0, n*2):
            temp = []
            if len(res) == 0:
                temp.append(('(', 1, 0))
                o -= 1 
            else:
                for r in res:
                    s, cur_open, cur_close = r 
                    if cur_open - cur_close > 0 and cur_close < n:
                        temp.append((s + ')', cur_open, cur_close + 1))
                    if cur_open < n:
                        temp.append((s + '(', cur_open + 1, cur_close))
            res = temp 
        return [s for s, _, _ in res]

                    


