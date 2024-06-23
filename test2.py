import uuid
import os
import json
from icecream import ic

class DrawTree:
    def __init__(self, string, level, file_name, parent=None, depth=0, number=1):
        # Node Configuration
        self.level = level
        self.depth = depth
        self.children = []
        self.mod = 0
        self.x = -1.0
        self.y = (self.depth * 500) + 400  # Automatically determining the position of the card here

        # Card Contents
        self.string = string
        self.file_name = file_name[:-3]  # dropping extension
        self.uuid = str(uuid.uuid4())
        self.title_content = self.string[self.level+1:-1]  # ignoring #, ## etc and the final newline

        # Card Configuration
        self.obsidian_json = {
            "id": self.uuid,
            "x": self.x,
            "y": self.y,
            "width": 400,
            "height": 400,
            "type": 'text',
            "text": self.string
        }

        # Tree Drawing Configuration
        self.parent = parent
        self.thread = None
        self.ancestor = self
        self.change = self.shift = 0
        self._lmost_sibling = None
        self.number = number

    def left(self):
        return self.thread or len(self.children) and self.children[0]

    def right(self):
        return self.thread or len(self.children) and self.children[-1]

    def lbrother(self):
        n = None
        if self.parent:
            for node in self.parent.children:
                if node == self:
                    return n
                else:
                    n = node
        return n

    def get_lmost_sibling(self):
        if not self._lmost_sibling and self.parent and self != self.parent.children[0]:
            self._lmost_sibling = self.parent.children[0]
        return self._lmost_sibling

    lmost_sibling = property(get_lmost_sibling)

    def __repr__(self, with_content=False):
        string = ''
        indent = "\t" * self.level
        string += f'{indent} Level: {self.level} Content: {self.title_content} X:{self.x}\n'

        if with_content:
            string += '\n' + indent + self.string

        return string

    def __str__(self):
        return self.__repr__()

    def modify_x(self, x):
        """Modifying the x-axis value for the card"""
        self.x = x
        self.obsidian_json['x'] = x

    def reflect_x(self):
        self.obsidian_json['x'] = self.x * 500

    def modify_node_string(self, new_string):
        self.string = new_string
        self.obsidian_json['text'] = self.string

    def add_children(self, child_node):
        if child_node.level == self.level + 1:
            x = len(self.children)
            child_node.x = x
            self.children.append(child_node)
        else:
            pass


def buchheim(tree):
    dt = firstwalk(tree)
    print('doing second walk')
    min_val = second_walk(dt)
    if min_val < 0:
        third_walk(dt, -min_val)
    return dt


def third_walk(tree, n):
    tree.x += n
    for c in tree.children:
        third_walk(c, n)


def firstwalk(v, distance=1.0):
    if len(v.children) == 0:
        if v.lmost_sibling:
            v.x = v.lbrother().x + distance
        else:
            v.x = 0.0
    else:
        default_ancestor = v.children[0]
        for w in v.children:
            firstwalk(w)
            default_ancestor = apportion(w, default_ancestor, distance)
        print("finished v =", v.string, "children")
        execute_shifts(v)

        midpoint = (v.children[0].x + v.children[-1].x) / 2

        w = v.lbrother()
        if w:
            v.x = w.x + distance
            v.mod = v.x - midpoint
        else:
            v.x = midpoint
    return v


def apportion(v, default_ancestor, distance):
    w = v.lbrother()
    if w is not None:
        vir = vor = v
        vil = w
        vol = v.lmost_sibling
        sir = sor = v.mod
        sil = vil.mod
        sol = vol.mod
        while vil.right() and vir.left():
            vil = vil.right()
            vir = vir.left()
            vol = vol.left()
            vor = vor.right()
            vor.ancestor = v
            shift = (vil.x + sil) - (vir.x + sir) + distance
            if shift > 0:
                move_subtree(ancestor(vil, v, default_ancestor), v, shift)
                sir = sir + shift
                sor = sor + shift
            sil += vil.mod
            sir += vir.mod
            sol += vol.mod
            sor += vor.mod
        if vil.right() and not vor.right():
            vor.thread = vil.right()
            vor.mod += sil - sor
        else:
            if vir.left() and not vol.left():
                vol.thread = vir.left()
                vol.mod += sir - sol
            default_ancestor = v
    return default_ancestor


def move_subtree(wl, wr, shift):
    subtrees = wr.number - wl.number
    print(wl.string, "is conflicted with", wr.string, "moving", subtrees, "shift", shift)
    wr.change -= shift / subtrees
    wr.shift += shift
    wl.change += shift / subtrees
    wr.x += shift
    wr.mod += shift


def execute_shifts(v):
    shift = change = 0
    for w in v.children[::-1]:
        print("shift:", w, shift, w.change)
        w.x += shift
        w.mod += shift
        change += w.change
        shift += w.shift + change


def ancestor(vil, v, default_ancestor):
    if vil.ancestor in v.parent.children:
        return vil.ancestor
    else:
        return default_ancestor


def second_walk(v, m=0, depth=0, min_val=None):
    v.x += m
    v.y = depth

    if min_val is None or v.x < min_val:
        min_val = v.x

    for w in v.children:
        min_val = second_walk(w, m + v.mod, depth + 1, min_val)

    return min_val


class Tree:
    def __init__(self, file_path):
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.canvas_json = {"nodes": [], "edges": []}
        self.max_depth_level = 0
        self.root_node = self.construct_tree()

    def get_file(self):
        file_path = self.file_path
        with open(file_path) as md_file:
            all_lines = md_file.readlines()
        return all_lines

    def construct_tree(self):
        all_lines = self.get_file()
        all_nodes = self.create_nodes_list(all_lines, self.file_name)
        tree_node = self._construct_tree(all_nodes)
        return tree_node

    def create_nodes_list(self, all_lines, file_name):
        root_node_content = file_name[:-2]
        root_node = DrawTree(root_node_content, 0, file_name)
        nodes = [root_node]

        current_node = None
        for line in all_lines:
            level = self.classify_header(line)
            if level > 0:
                node = DrawTree(line, level, file_name)
                nodes.append(node)
                current_node = node
            else:
                if current_node is not None:
                    new_string = current_node.string + line
                    current_node.modify_node_string(new_string)

        return nodes

    def _construct_tree(self, node_list):
        for idx in range(len(node_list) - 1, 0, -1):
            node = node_list[idx]
            self.max_depth_level = max(self.max_depth_level, node.level)

            for candidate_idx in range(idx, -1, -1):
                candidate_node = node_list[candidate_idx]

                if candidate_node.level == node.level - 1:
                    candidate_node.add_children(node)
                    break

        return node_list[0]

    def obsidian_construct_cards(self, node):
        print()
        print("Before")
        print(node.obsidian_json['x'])
        node.modify_x(node.x * 500)
        print("After")
        print(node.obsidian_json['x'])

        self.canvas_json['nodes'].append(node.obsidian_json)

        children_nodes = node.children
        if len(children_nodes) > 0:
            for child in children_nodes:
                self.obsidian_construct_cards(child)

        return self.canvas_json

    def _obsidian_connect_edges(self, node):
        for child_node in node.children:
            edge_dict = {
                "id": str(uuid.uuid4()),
                "fromNode": node.uuid,
                "fromSide": "bottom",
                "toNode": child_node.uuid,
                "toSide": "top"
            }
            self.canvas_json['edges'].append(edge_dict)

            if len(child_node.children) > 0:
                self._obsidian_connect_edges(child_node)

    @staticmethod
    def classify_header(line: str) -> int:
        """Classify the level of the markdown header"""
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
            return -1


def print_tree(node):
    print(node)
    if len(node.children) > 0:
        for child in node.children:
            print_tree(child)
    else:
        pass


def poc_verify(node):
    final_x = node.x
    node.modify_x(final_x * 500)
    children_nodes = node.children

    if node.level == 2:
        print("Level 2")
        print(node.title_content)
        print([i.title_content for i in children_nodes])
        for child in children_nodes:
            print(child.title_content, '\t', node.x, node.obsidian_json['x'])
        print()
    if len(children_nodes) > 0:
        for child in children_nodes:
            poc_verify(child)


if __name__ == "__main__":
    file_path = './media/4.Data Engineering.md'
    tree = Tree(file_path)

    print('------------------------------------------------')
    painted_root_node = buchheim(tree.root_node)

    print_tree(painted_root_node)

    tree.obsidian_construct_cards(painted_root_node)
    tree._obsidian_connect_edges(painted_root_node)

    canvas_path = r"C:\Users\viren\Documents\Obsidian Vault\Archive\Semester V\Principles of Data Science & Engineering\june_3_2024.canvas"
    with open(canvas_path, 'w') as json_file:
        json.dump(tree.canvas_json, json_file)
