class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        if head is None or head.next is None:
            return head 
        pr, first, second = None, head, head.next 
        while first is not None and second is not None: 
            nxt = second.next 
            second.next = first 
            first.next = nxt 
            if pr is None:
                head = second 
            else:
                pr.next = second 
            pr = first 
            first = first.next 
            second = first.next if first is not None else None 
        return head 