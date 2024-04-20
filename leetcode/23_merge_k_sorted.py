# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
import heapq

class Solution(object):
    def getMin(self, lists):
        n = None 
        for idx, l in enumerate(lists):
            if l is not None:
                n = (idx, l) if n is None or n[1].val > l.val else n 
        return n 
    def insert(self, lists, n):
        pass

    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        heap = []
        head, tail = None, None
        for n in lists:
            if n is not None:
                heapq.heappush(heap, (n.val, n))
        while len(heap) > 0:
            _, n = heapq.heappop(heap)
            if head is None:
                head = n 
            if tail is not None:
                tail.next = n 
            tail = n 
            if n.next is not None:
                heapq.heappush(heap, (n.next.val, n.next)) 
        return head 

    def mergeKLists2(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        cur = self.getMin(lists)
        if cur is None:
            return None
        head, tail = cur[1], None
        
        while cur is not None:
            if tail is not None:
                tail.next = cur[1]            
            tail = cur[1]
            lists[cur[0]] = cur[1].next
            nextMin = self.getMin(lists)            
            cur = nextMin
        return head 
            
### NOTE: there is another acceptable way is to use merge sort. Merge a pair of array
            
            
        
