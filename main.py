from icecream import ic
import uuid
import os
import json
from node import Node


nexts =[0]*4 # hardcoded max depth level for now

class Tree:
    def __init__(self,file_path):

        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.canvas_json = {"nodes":[],	"edges":[] }
        self.max_depth_level = 0
        self.root_node = self.construct_tree()
        
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
                # the line is not a level changing line, append it to current node if it exists.
                if current_node != None:   
                    
                    new_string = current_node.string + line
                    current_node.modify_node_string(new_string)
            
        return nodes

    def _construct_tree(self,node_list):    
    
        for idx in range(len(node_list)-1,0,-1):
            
            # taking node, find the parent and the append the node to the parent.
            node = node_list[idx]
            self.max_depth_level = max(self.max_depth_level,node.level)
            
            for candidate_idx in range(idx,-1,-1):
                candidate_node = node_list[candidate_idx]
                
                if candidate_node.level == node.level - 1:
                    candidate_node.add_children(node)
                    break
        
    
        return node_list[0]

    def obsidian_construct_cards(self,node):
        
        self.canvas_json['nodes'].append(node.obsidian_json)
        children_nodes = node.children

        if len(children_nodes) > 0:
            for child in children_nodes:
                self.obsidian_construct_cards(child)
        
        return self.canvas_json

    def _obsidian_connect_edges(self,node):

        for child_node in node.children:
            edge_dict = {"id":str(uuid.uuid4()),
                         "fromNode":node.uuid,
                         "fromSide":"bottom",
                         "toNode":child_node.uuid,
                         "toSide":"top"}
            self.canvas_json['edges'].append(edge_dict)
            
            if len(child_node.children) > 0:
                self._obsidian_connect_edges(child_node)

    @staticmethod
    def assign_x(node):
        global nexts 

        level = node.level
        node.modify_x(nexts[level] * 700)
        ic(level,nexts[level])        
        nexts[level] += 1
        ic(level,nexts[level])        
        print()

        for c in node.children:
            Tree.assign_x(c)
        






def print_tree(node):
    print(node)
    if len(node.children) > 0:
        for child in node.children:
            print_tree(child)
    else:
        pass
            


if __name__ == "__main__":
    
    file_path = './media/4.Data Engineering.md'
    tree = Tree(file_path)
    tree.obsidian_construct_cards(tree.root_node)
    tree._obsidian_connect_edges(tree.root_node)
    
    # print(tree.canvas_json)
    tree.assign_x(tree.root_node)

    canvas_path = r"C:\Users\viren\Documents\Obsidian Vault\Archive\Semester V\Principles of Data Science & Engineering\april_2024.canvas"
    with open(canvas_path,'w') as json_file:
        json.dump(tree.canvas_json,json_file)

    print()
    print_tree(tree.root_node)

    print()
    # tree.parent_over_child(tree.root_node)
    print_tree(tree.root_node)
    
    
    
    
    
