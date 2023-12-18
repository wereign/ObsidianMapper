
file_path = './media/4.Data Engineering.md'

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
        return -1 # using 0 as file node level.

class Node:
    def __init__(self,string,level):
        self.level = level
        self.string = string
        self.children = []
    
    def add_children(self,child_node):
        
        if child_node.level == self.level + 1:
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

def create_nodes_list(all_lines,file_name):

    root_node_content = file_name[:-2]
    root_node = Node(root_node_content,level=0)
    nodes = [root_node]
    for line in all_lines:

        level = classify_header(line)

        if level > 0:

            node = Node(line,level)
            nodes.append(node)
    
    return nodes

all_lines = get_file(file_path)

all_nodes = create_nodes_list(all_lines,file_path) # file name and path will be different eventually


def construct_tree(node_list):
    
    for idx in range(len(node_list)-1,0,-1):
        
        # taking node, find the parent and the append the node to the parent.
        node = node_list[idx]
        for candidate_idx in range(idx,-1,-1):
            candidate_node = node_list[candidate_idx]
            
            if candidate_node.level == node.level - 1:
                candidate_node.add_children(node)
                break
    
    
    return node_list[0]

root_node = construct_tree(all_nodes)

print(root_node)
print(root_node.children)

    