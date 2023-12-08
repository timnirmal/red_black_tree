class Node:
    def __init__(self, key, color="red", left=None, right=None, parent=None):
        self.key = key
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent


class RedBlackTree:
    def __init__(self):
        self.nil = Node(key=None, color="black")
        self.root = self.nil

    @staticmethod
    def grandparent(n):
        if n.parent is None:
            return None
        return n.parent.parent

    def uncle(self, n):
        g = self.grandparent(n)
        if g is None:
            return None
        if n.parent == g.left:
            return g.right
        return g.left

    def search(self, key):
        node = self.root
        while node != self.nil and key != node.key:
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def maximum(self, node):
        while node.right != self.nil:
            node = node.right
        return node

    def minimum(self, node):
        while node.left != self.nil:
            node = node.left
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def insert(self, key):
        node = Node(key)
        node.left = self.nil
        node.right = self.nil
        y = None
        x = self.root

        while x != self.nil:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.color = "red"
        self.fix_insertion(node)

    def fix_insertion(self, z):
        while z.parent is not None and z.parent.color == "red":
            if z.parent == self.grandparent(z).left:
                y = self.uncle(z)
                if y is not None and y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    self.grandparent(z).color = "red"
                    z = self.grandparent(z)
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "black"
                    self.grandparent(z).color = "red"
                    self.right_rotate(self.grandparent(z))
            else:
                y = self.uncle(z)
                if y is not None and y.color == "red":
                    z.parent.color = "black"
                    y.color = "black"
                    self.grandparent(z).color = "red"
                    z = self.grandparent(z)
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "black"
                    self.grandparent(z).color = "red"
                    self.left_rotate(self.grandparent(z))

            if z == self.root:
                break
        self.root.color = "black"

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.search(key)
        if z == self.nil:
            return

        y = z
        y_original_color = y.color
        if z.left == self.nil:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)  # Find the node with the minimum key in the right subtree.
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "black":
            self.fix_deletion(x)

    def fix_deletion(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == "black" and w.right.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.right.color == "black":
                        w.left.color = "black"
                        w.color = "red"
                        self.right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "red":
                    w.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == "black" and w.left.color == "black":
                    w.color = "red"
                    x = x.parent
                else:
                    if w.left.color == "black":
                        w.right.color = "black"
                        w.color = "red"
                        self.left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = "black"
                    w.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "black"

    def print_tree(self, node, indent="", last=True):
        # Check if the current node is the NIL node
        if node == self.nil:
            return

        # if node color is red, new variable, color = "R", else color = "B"
        color = "R" if node.color == "red" else "B"

        # Handle the root node separately
        if node == self.root:
            print(color + str(node.key))
        else:
            # Print the tree structure for non-root nodes
            branch = "└──" if last else "├──"
            print(indent + branch + color + str(node.key))
            indent += "   " if last else "│  "

        # Print the right subtree
        if node.right and node.right != self.nil:
            self.print_tree(node.right, indent, False)

        # Print the left subtree
        if node.left and node.left != self.nil:
            self.print_tree(node.left, indent, True)


def handle_command(rbt, command):
    if command.startswith("Delete "):
        _, value = command.split()
        rbt.delete(int(value))
        rbt.print_tree(rbt.root)
    elif command.startswith("Search "):
        _, value = command.split()
        result = rbt.search(int(value))
        print("True" if result != rbt.nil else "False")
    elif command == "Max":
        max_node = rbt.maximum(rbt.root)
        print("Maximum value:", max_node.key if max_node != rbt.nil else "Tree is empty")
    elif command == "Min":
        min_node = rbt.minimum(rbt.root)
        print("Minimum value:", min_node.key if min_node != rbt.nil else "Tree is empty")
    elif command == "Print":
        rbt.print_tree(rbt.root)


def run_red_black_tree_console():
    rbt = None
    while True:
        command = input("Enter command (or 'Exit' to quit): ").strip()

        # Exit condition
        if command.lower() in ["exit", "e"]:
            break

        # Initialize the tree if needed
        if not rbt and all(c.isdigit() or c.isspace() for c in command):
            numbers = [int(num) for num in command.split()]
            rbt = RedBlackTree()
            for num in numbers:
                rbt.insert(num)
            rbt.print_tree(rbt.root)
        elif rbt:
            if command.isdigit():
                num_operations = int(command)
                print(f"Enter {num_operations} operations:")
                for _ in range(num_operations):
                    op_command = input("> ")
                    handle_command(rbt, op_command)
            else:
                handle_command(rbt, command)
        else:
            print("Please initialize the tree first by entering numbers.")


if __name__ == "__main__":
    run_red_black_tree_console()
