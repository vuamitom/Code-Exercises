class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if len(nums) < 4:
            return [] 
        nums = sorted(nums)
        res = set()
        for i in range(0, len(nums)):
            for j in range(i + 1, len(nums)):
                x = j + 1
                y = len(nums) - 1
                s = target - nums[i] - nums[j]
                while x < y:
                    t = nums[x] + nums[y]
                    if t < s:
                        x += 1
                    elif t > s:
                        y -= 1
                    else:
                        res.add((nums[i], nums[j], nums[x], nums[y]))
                        x += 1
                        y -= 1
        return res 

                    

        