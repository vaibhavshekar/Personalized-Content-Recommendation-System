class TreeNode:
    def __init__(self, value):
        self.parent = None
        self.left = None
        self.right = None
        self.value = value

class maxHeap:
    def __init__(self):
        self.root = None

    # Insertion operation
    def insert_element(self, reel_id, weight):
        new_node = TreeNode((reel_id, weight))
        if self.root is None:
            self.root = new_node
        else:
            last_parent = self._find_last_parent()
            if last_parent.left is None:
                last_parent.left = new_node
            else:
                last_parent.right = new_node
            new_node.parent = last_parent
            self._bubble_up(new_node)

    # Helper method to find the last parent node in the heap
    def _find_last_parent(self):
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None or current.right is None:
                return current
            queue.append(current.left)
            queue.append(current.right)

    # Bubble up operation to maintain heap property after insertion
    def _bubble_up(self, node):
        while node.parent is not None and node.value[1] > node.parent.value[1]:
            node.value, node.parent.value = node.parent.value, node.value
            node = node.parent

    # Heapify operation
    def heapify(self, node):
        largest = node
        if node.left is not None and node.left.value[1] > largest.value[1]:
            largest = node.left
        if node.right is not None and node.right.value[1] > largest.value[1]:
            largest = node.right
        if largest != node:
            node.value, largest.value = largest.value, node.value
            self.heapify(largest)

    # Extract max operation
    def extract_max(self):
        if self.root is None:
            return None
        max_value = self.root.value
        last_node = self._find_last_node()
        if last_node != self.root:
            self.root.value = last_node.value
            if last_node.parent.left == last_node:
                last_node.parent.left = None
            else:
                last_node.parent.right = None
            self.heapify(self.root)
        else:
            self.root = None
        return max_value

    # Helper method to find the last node in the heap
    def _find_last_node(self):
        if self.root is None:
            return None
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.left is None and current.right is None:
                return current
            if current.left is not None:
                queue.append(current.left)
            if current.right is not None:
                queue.append(current.right)

    def create_heap(self, tuples):
        for reel_id, weight in tuples:
            self.insert_element(reel_id, weight)