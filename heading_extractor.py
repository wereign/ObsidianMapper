import uuid
import os

file_path = './media/4.Data Engineering.md'




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


class TreeFunctions:
    def __init__(self,file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = self.file_path
        
    
    def get_file(self):
        file_path = self.file_path
        with open(file_path) as md_file:
            all_lines = md_file.readlines()
        return all_lines
    
    def construct_tree(self):

        all_lines = self.get_file()
        all_nodes = self.create_nodes_list(all_lines,self.file_name)
        tree_node = self.construct_tree(all_nodes)

        return tree_node
    
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    