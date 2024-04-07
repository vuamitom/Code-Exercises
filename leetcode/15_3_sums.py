class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        m = {v: k for k, v in enumerate(nums)}
        r = set()
        for i in range(0, len(nums)):
            for j in range(i+1, len(nums)):
                c = 0 - (nums[i] + nums[j])
                if c in m and m[c] > j:
                    r.add(tuple(sorted((nums[i], nums[j], c))))
        return r 
    

class Solution2(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        r = []
        tried = set()
        for i, x in enumerate(nums):
            if x not in tried:
                self.twoSum(nums, i+1, 0 - x, r)                
                tried.add(x)
        return set([tuple(sorted(t)) for t in r])

    def twoSum(self, nums, fr, total, r):
        temp = set() 
        for i in range(fr, len(nums)):
            n = nums[i] 
            if total - n in temp: 
                r.append((n, total-n, 0 - total))
            else:
                temp.add(n)
        return None 
