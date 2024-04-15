import uuid
import os
import json


class Node:
    def __init__(self,string,level,file_name):
        
        # Node Configuration
        self.level = level
        self.children = []
        self.mod = 0
        self.x = 0
        self.y = (self.level * 500) + 400 # Automatically determining the position of the card here
        # 500 is for the height of the card, and 400 for the distance between the cards

        # Card Contents
        self.string = string
        self.file_name = file_name[:-3] # dropping extension
        self.uuid = str(uuid.uuid4())
        self.title_content = self.string[self.level+1:-1] # ignoring #, ## etc and the final newline
        

        # Card Configuration

        self.obsidian_json = {
            "id":self.uuid,
            "x":self.x,
            "y":self.y,
            "width":400,
            "height":400,
            "type":'text',
            "text":self.string
        }

    
    def modify_node_string(self,new_string):
        self.string = new_string
        self.obsidian_json['text'] = self.string
    
    def add_children(self,child_node):
        
        if child_node.level == self.level + 1:
            x = len(self.children)
            child_node.x = x
            self.children.append(child_node)
        else:
            pass
    
    def __repr__(self,with_content=False):

        string = ''
        indent="\t"*self.level
        string += f'{indent} Level: {self.level} Content: {self.title_content} X:{self.x}\n'

        if with_content:
            string += '\n'+indent+self.string

        return string   
    
    def __str__(self):

        return self.__repr__()

    def modify_x(self,x):

        """Modifying the x axis value for the card"""
        self.x = x
        self.obsidian_json['x'] = x
