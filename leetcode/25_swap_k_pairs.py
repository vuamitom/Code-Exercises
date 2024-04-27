# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        buffer = [None] * k 
        c = 0 
        cur = head 
        prev = None
        while cur is not None:
            buffer[c] = cur 
            c += 1 
            cur = cur.next 
            if c == k:
                # swap
                for i in reversed(range(1, k)):                    
                    buffer[i].next = buffer[i - 1]
                if prev is None:
                    head = buffer[k - 1]                    
                else:
                    prev.next = buffer[k - 1]
                prev = buffer[0]
                prev.next = None
                c = 0
        if c > 0 and prev is not None:
            prev.next = buffer[0]
        return head 