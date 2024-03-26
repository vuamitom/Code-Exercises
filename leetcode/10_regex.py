class Solution(object):
    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        pis = [(0, 0)]
        while len(pis) > 0:
            pp = set()
            print (pis)
            for si, pi in pis:
                if si >= len(s) and (pi >= len(p) or (pi == len(p) - 2 and p[pi + 1] == '*')):
                    return True 
                elif pi >= len(p):
                    continue
                cp, cs = p[pi], s[si] if si < len(s) else None
                m = p[pi + 1] if pi < len(p) - 1 else None
                if m == '*':                    
                    pp.add((si, pi+2))
                    if cp == cs or (cp == '.' and cs is not None):                        
                        pp.add((si + 1, pi))                                            
                else:
                    if cp == cs or (cp == '.' and cs is not None):
                        pp.add((si + 1, pi + 1))                    
            pis = pp 
        return False 
    
    def isMatch2(self, s, p):
        pass 