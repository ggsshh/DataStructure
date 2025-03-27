class Node:
    def __init__(self, data_x, data_y):
        self.data = (data_x, data_y)
        self.next = None


class Linked_List:
    def __init__(self):
        self.cur = None
        self.length = 0

    def add(self, data_x, data_y):
        node = Node(data_x, data_y)
        if self.length == 0:
            self.cur = node
            self.cur.next = self.cur
            self.length += 1
        else:
            node.next = self.cur.next
            self.cur.next = node
            self.cur = self.cur.next
            self.length += 1

    def move_and_extract(self, value):
        count = 0
        while count < value:
            self.cur = self.cur.next
            count += 1
        return self.cur.data
