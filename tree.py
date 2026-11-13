class Node:
    def __init__(self, value) -> None:
        self.value = value
        self.left: Node | None = None
        self.right: Node | None = None


def get_spacing(depth):
    first_num_spacing = 2**depth
    other_num_spacing = 0
    if depth == 1:
        other_num_spacing = 3
    elif depth == 2:
        other_num_spacing = 7
    elif depth == 3:
        other_num_spacing = 15
    elif depth == 4:
        other_num_spacing = 31
    return [first_num_spacing, other_num_spacing]


def print_tree(node, depth):
    layer_nodes = [node]
    while len(layer_nodes) > 0:
        layer_has_nodes = False
        next_layer_nodes = []
        current_values = []
        spacing = get_spacing(depth)
        first_num_spacing = spacing[0]
        other_num_spacing = spacing[1]
        for i in range(len(layer_nodes)):
            n = layer_nodes[i]
            if n is not None:
                layer_has_nodes = True
                if n.left != None:
                    next_layer_nodes.append(n.left)
                else:
                    next_layer_nodes.append(None)
                if n.right != None:
                    next_layer_nodes.append(n.right)
                else:
                    next_layer_nodes.append(None)
                # make every number two chars long
                svalue = str(n.value).rjust(2, " ")
            else:
                svalue = "  "
            # spacing for layers
            print(current_values, i)
            if len(current_values) == 0:
                svalue = svalue.rjust(first_num_spacing)
            else:
                svalue = svalue.rjust(other_num_spacing)
            current_values.append(svalue)
        if layer_has_nodes:
            print(" ".join(current_values))
        layer_nodes = next_layer_nodes
        depth = depth - 1


def main():
    leaf1 = Node(-5)
    leaf2 = Node(7)
    leaf3 = Node(15)
    leaf4 = Node(14)
    leaf5 = Node(8)
    leaf6 = Node(-5)
    leaf7 = Node(1)
    leaf8 = Node(0)

    body3_1 = Node(3)
    body3_1.left = leaf1
    body3_1.right = leaf2

    body3_2 = Node(20)
    body3_2.left = leaf3
    body3_2.right = leaf4

    body3_3 = Node(-8)
    body3_3.left = leaf5
    body3_3.right = leaf6

    body3_4 = Node(-1)
    body3_4.left = leaf7
    body3_4.right = leaf8

    body2_1 = Node(-2)
    body2_1.left = body3_1
    body2_1.right = body3_2

    body2_2 = Node(10)
    body2_2.left = body3_3
    body2_2.right = body3_4

    root = Node(None)
    root.left = body2_1
    root.right = body2_2

    print_tree(root, 4)


if __name__ == "__main__":
    main()
