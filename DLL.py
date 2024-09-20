import tarfile


class Node:
    def __init__(self, data) :
        self.data = data
        self.next = None
        self.prev = None

class DLL:
    def __init__(self):
        self.head = None
        self.tail = None

    def isEmpty(self):
        return self.head is None
    
    def insertFirst(self,data):
        new_node = Node(data)
        if self.isEmpty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def insertLast(self,data):
        newNode = Node(data)
        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            self.tail.next = newNode
            newNode.prev = self.tail
            self.tail = newNode
    
    def deleteLast(self):
        if self.isEmpty():
            print("List is Empty")
            return
        
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

    def deleteFirst(self):
        if self.isEmpty():
            print("List is Empty")
            return
        
        if self.head == self.tail:
            self.head = None
            self.tail = None

        else:
            self.head = self.head.next
            self.head.prev = None

    def traverse(self):
        current = self.head
        while current:
            print(current.data, end="\n")
            current = current.next
        print(None)

dl = DLL()
dl.insertFirst(10)
dl.insertLast(20)
dl.insertFirst(5)
dl.insertLast(30)
dl.traverse()
dl.deleteLast()
dl.traverse()