
file_path = './4.Data Engineering.md'

def get_file(file_path:str):
    with open(file_path) as md_file:
        all_lines = md_file.readlines()
    return all_lines

def classify_header(line):   
    h1_id = '# '
    h2_id = '## '
    h3_id = '### '

    if line[:len(h1_id)] == h1_id:
        return 1

    elif line[:len(h2_id)] == h2_id:
        return 2

    elif line[:len(h3_id)] == h3_id:
        return 3

    else:
        return 0

class Node:
    def __init__(self,string,level):
        self.level = level
        self.string = string
        self.children = []
    
    def add_children(self,child_node):
        
        if child_node.level == self.level - 1:
            self.children.append(child_node)
        else:
            pass
    
    def __repr__(self):

        string = ''
        indent="\t"*self.level
        string += f'{indent}Level: {self.level}\n{indent}Content: {self.string}'

        return string   
    
    def __str__(self):

        return self.__repr__()

def create_nodes_list(all_lines):

    nodes = []
    for line in all_lines:

        level = classify_header(line)

        if level > 0:

            node = Node(line,level)
            nodes.append(node)
    
    return nodes

all_lines = get_file(file_path)

all_nodes = create_nodes_list(all_lines)

for node in all_nodes:
    print(node)

    