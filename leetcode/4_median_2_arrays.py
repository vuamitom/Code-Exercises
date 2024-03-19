import bisect
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        
        count, c, p1, p2 = 0, None, 0, 0
        total = len(nums1) + len(nums2)
        m = total / 2
        prev = None
        while count <= m:
            if p2 >= len(nums2) or (p1 < len(nums1) and nums1[p1] < nums2[p2]):
                prev = c
                c = (p1, nums1)
                p1 += 1
            else: 
                prev = c 
                c = (p2, nums2)
                p2 += 1 
            count += 1
        if total % 2 == 1:
            p, ar = c 
            return ar[p]
        else:
            p, ar = c
            pp, par = prev 
            return (ar[p] + par[pp]) / 2.0

    ## This method is not working for all cases 
    def findMedianSortedArrays2(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        count, c, p1, p2 = 0, None, 0, 0
        total = len(nums1) + len(nums2)
        m = (total + 1) / 2
        prev = None
        while count <= m:
            if p2 >= len(nums2):                                
                if m - count - 1 >= p1:
                    prev = (m - count - 1, nums1)
                else:
                    prev = c 
                c = (m - count, nums1)
                count = m + 1
            elif p1 >= len(nums1):
                if m - count - 1 >= p2:
                    prev = (m - count - 1, nums2)
                else:
                    prev = c 
                c = (m - count, nums2)
                count = m + 1
            elif nums1[p1] < nums2[p2]:
                next = bisect.bisect_left(nums1, nums2[p2], p1)  
                print ('>> ',next, p1)                              
                count += next - p1 if next > p1 else 1 
                if count > m:
                    next -= count - m
                if next - 2 >= p1:                
                    prev = (next-2, nums1)
                else:
                    prev = c
                c = (next - 1 if next > p1 else next, nums1)                                                                               
                print('> 1', next, p1, count, p2)
                p1 = next + 1 if next == p1 else next          
            else:                 
                next = bisect.bisect_left(nums2, nums1[p1], p2)   
                print ('>>.. ',next, p1, p2)                             
                count += next - p2  if next > p2 else 1
                if count > m:
                    next -= count - m  
                if next - 2 >= p2:
                    prev = (next - 2 , nums2)
                else:
                    prev = c
                c = (next - 1 if next > p2 else next, nums2)                
                p2 = next + 1 if next == p2 else next 
                print('> 2', next, p2, count, p1, c)
                
            
        if total % 2 == 1:
            p, ar = c 
            return ar[p]
        else:
            p, ar = c
            pp, par = prev 
            return (ar[p] + par[pp]) / 2.0
        
