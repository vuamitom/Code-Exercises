class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        s, e = 0, len(height) - 1 
        area = None
        while s < e: 
            m = min(height[s], height[e]) * (e - s)
            area = m if area is None or area < m else area 
            if height[s] < height[e]:
                s += 1 
            else:
                e -= 1
        return area


        