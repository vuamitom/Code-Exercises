class Solution(object):
    
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        ml = min([len(s) for s in strs])
        i = 0 
        common = []
        while i < ml:
            p = None
            diff = False 
            for j in range(1, len(strs)):
                if not strs[j][i] == strs[j-1][i]:
                    diff = True
                    break 
            if not diff:
                common.append(strs[0][i])
            else:
                break 
            i+= 1
        return ''.join(common)
    
    # This is a better solution 
    # in case strs is longer list than an average string in the list 
    def longestCommonPrefix(self, v: List[str]) -> str:
        ans=""
        v=sorted(v)
        first=v[0]
        last=v[-1]
        for i in range(min(len(first),len(last))):
            if(first[i]!=last[i]):
                return ans
            ans+=first[i]
        return ans 
