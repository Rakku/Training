

class Tree():
    def __init__(self):
        self.root = Node()

    def walk(self, node=None):
        node = node or self.root
        yield node
        for child in node.children:
            for n in walk(child):
                yield n

    def add_node(self, node, parent):
        parent.children.append(node)

class Node():
    def __init__(self, name):
        self.name = name
        self.children = []