def get_last_index(name, node_list):
    for i in range(len(node_list)):
        if name == node_list[i]:
            return i
    return

def get_children(index, side_list, node_list):
    result = []
    for i in range(len(side_list)):
        if side_list[i][0] == index:
            result.append(node_list[side_list[i][1]])
    return result

def traverse(nodes, sides):
    forks = []
    output = []
    current = []

    if not len(nodes):
        return
    output.append(nodes[0])

    has_no_children = False
    while len(output):
        next_obj = output[-1]
        next_index = get_last_index(next_obj, nodes)
        if has_no_children:
            has_no_children = False
            print([int(item) for item in output])
            while len(output) and (
                len(forks) <= 0
                or output[-1]
                != forks[-1]
            ):
                transfer = output.pop()
            if len(forks):
                forks.pop()
        else:
            children = get_children(next_index, sides, nodes)
            if len(children):
                for i in range(len(children)):
                    current.append(children[i])
                    if i:
                        forks.append(next_obj)
            else:
                has_no_children = True
                continue
        if len(current):
            transfer = current.pop()
            output.append(transfer)

nodes = [str(item + 1) for item in range(0, 8)]
sides = [[0, 2],
            [0, 1],
            [1, 4],
            [1, 3],
            [2, 5],
            [3, 7],
            [4, 7],
            [4, 6],
            [4, 5],
            [4, 3],
            [5, 6],
            [6, 7]]

traverse(nodes, sides)