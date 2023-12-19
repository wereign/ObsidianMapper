import uuid
import os
import json
file_path = './media/4.Data Engineering.md'

class Node:
    def __init__(self,string,level,file_name):
        self.level = level
        self.string = string
        self.file_name = file_name[:-3] # dropping extension
        self.uuid = str(uuid.uuid4())
        self.title_content = self.string[self.level+1:-1] # ignoring #, ## etc and the final newline
        
        self.obsidian_json = {
            "id":self.uuid,
            "x":0,
            "y":0,
            "width":400,
            "height":400,
            "type":'text',
            # "text":f"![[{self.file_name}#{self.title_content}]]"
            "text":self.string
        }

        self.children = []
    
    def modify_node_string(self,new_string):
        self.string = new_string
        self.obsidian_json['text'] = self.string
    
    def add_children(self,child_node):
        
        if child_node.level == self.level + 1:
            self.children.append(child_node)
        else:
            pass
    
    def __repr__(self,with_content=False):

        string = ''
        indent="\t"*self.level
        string += f'{indent}Level: {self.level} Content: {self.title_content}'

        if with_content:
            string += '\n'+indent+self.string

        return string   
    
    def __str__(self):

        return self.__repr__()

    def modify_position(self,x,y):
        
        self.obsidian_json['x'] = x
        self.obsidian_json['y'] = y
        
class Tree:
    def __init__(self,file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.root_node = self.construct_tree()
        self.canvas_json = {"nodes":[],	"edges":[] }
        
    def get_file(self):
        file_path = self.file_path
        with open(file_path) as md_file:
            all_lines = md_file.readlines()
        return all_lines

    def construct_tree(self):

        all_lines = self.get_file()
        all_nodes = self.create_nodes_list(all_lines,self.file_name)
        tree_node = self._construct_tree(all_nodes)

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

    def create_nodes_list(self,all_lines,file_name):

        root_node_content = file_name[:-2]
        root_node = Node(root_node_content,0,file_name)
        nodes = [root_node]

        current_node = None
        for line in all_lines:

            level = self.classify_header(line)
            if level > 0:
                node = Node(line,level,file_name)
                nodes.append(node)
                current_node = node
            else:
                if current_node != None:
                    # print(current_node)
                    new_string = current_node.string + line
                    current_node.modify_node_string(new_string)
            
        return nodes

    @staticmethod
    def _construct_tree(node_list):
    
        for idx in range(len(node_list)-1,0,-1):
            
            # taking node, find the parent and the append the node to the parent.
            node = node_list[idx]
            for candidate_idx in range(idx,-1,-1):
                candidate_node = node_list[candidate_idx]
                
                if candidate_node.level == node.level - 1:
                    candidate_node.add_children(node)
                    break
        
    
        return node_list[0]

    def construct_cards(self,node):
        
        self.canvas_json['nodes'].append(node.obsidian_json)
        children_nodes = node.children

        if len(children_nodes) > 0:
            for child in children_nodes:
                self.construct_cards(child)
        
        return self.canvas_json

    def _connect_edges(self,node):

        for child_node in node.children:
            edge_dict = {"id":str(uuid.uuid4()),
                         "fromNode":node.uuid,
                         "fromSide":"bottom",
                         "toNode":child_node.uuid,
                         "toSide":"top"}
            self.canvas_json['edges'].append(edge_dict)
            
            print(child_node.title_content)
            print(child_node.children)
            if len(child_node.children) > 0:
                self._connect_edges(child_node)

        

def print_tree(node):

    print(node.title_content)

    if len(node.children) > 0:

        for child in node.children:
            
            print_tree(child)
    else:
        pass
            


if __name__ == "__main__":
    
    tree = Tree(file_path)
    tree.construct_cards(tree.root_node)
    tree._connect_edges(tree.root_node)
    
    # print(tree.canvas_json)
    with open('./some_file.canvas','w') as json_file:
        json.dump(tree.canvas_json,json_file)

    print()
    print()
    print_tree(tree.root_node)
    
    
    
    
    
