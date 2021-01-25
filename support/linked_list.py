# Basic linked list and node objects

class Node:
    def __init__(self, val=None, next=None):
        self.val = val
        self.next = next

class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def fill(self, num: int):
        '''
        Fills LinkedList with given number of incrementing values

        :param num: Number of nodes to ask
        '''
        if num == 0:
            return

        self.next = Node(0)
        curr = self.next
        for i in range(1, num):
            curr.next = Node(i)
            curr = curr.next
