from paper import buchheim
import matplotlib.pyplot as plt

# Assuming the DrawTree and TreeNode classes and the Buchheim algorithm are already defined and imported.

class TreeNode:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children if children is not None else []

# Define a simple tree
root = TreeNode("root", [
    TreeNode("child1", [
        TreeNode("child1.1"),
        TreeNode("child1.2"),
    ]),
    TreeNode("child2", [
        TreeNode("child2.1")
    ]),
    TreeNode("child3")
])

# Run the Buchheim algorithm
draw_tree = buchheim(root)

# Helper function to extract coordinates and draw the tree
def plot_tree(node, ax):
    if node.parent:
        ax.plot([node.x, node.parent.x], [node.y, node.parent.y], 'k-')
    ax.text(node.x, node.y, str(node.tree.value), ha='center', va='center', bbox=dict(facecolor='white', edgecolor='black'))
    for child in node.children:
        plot_tree(child, ax)

# Plot the tree
fig, ax = plt.subplots()
ax.invert_yaxis()  # Invert y-axis to have root on top
plot_tree(draw_tree, ax)
plt.show()
