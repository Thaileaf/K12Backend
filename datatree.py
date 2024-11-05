class TreeNode:
    def __init__(self, content="", topic=""):
        self.topic = topic
        self.content = content
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)
        
    def __str__(self, level=0):
        ret = "  " * level + self.topic + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

def build_tree(data):
    if not data:
        return None
        
    root = TreeNode(content=data[0][-1])  # Create root with first non-empty content
    current_path = [root]  # Stack to keep track of current path
    prev_depth = 0
    
    # Start from index 1 to skip the root
    for line in data[1:]:
        if not any(line):  # Skip empty lines
            continue
            
        # Calculate depth by counting empty strings
        depth = 0
        for item in line:
            if item == '':
                depth += 1
            else:
                break
                
        content = line[depth] if depth < len(line) else ""
        
        # Create new node
        split_content = content.split("\n")
        if len(split_content) > 1:
            content = split_content[1]
            topic = split_content[0]
            new_node = TreeNode(content, topic)
        else:
            new_node = TreeNode(content=split_content[0])
        
        # Adjust current path based on depth
        if depth > prev_depth:
            # Add as child to previous node
            current_path[-1].add_child(new_node)
        elif depth == prev_depth:
            # Sibling of previous node
            current_path.pop()
            current_path[-1].add_child(new_node)
        else:
            # Go back up the tree
            while len(current_path) > depth:
                current_path.pop()
            current_path[-1].add_child(new_node)
            
        current_path.append(new_node)
        prev_depth = depth
        
    return root



# Example usage
def example_usage():
    data = [
        ['Welcome to K12 Center, what would you like to know about'],
        ['', 'Programs\nPrograms at K12...', ' '],
        ['', 'Cost\nA lot....'],
        ['', '', 'Sponserships\nMaybe...'],
        ['', '', '', 'Testing\nTesting'],
        ['', '', '', 'Testing\nTesting'],
        ['', '', '', 'Testing\nTesting'],
        ['', '', 'Sponserships\nMaybe...'],
        ['', '', 'Sponserships\nMaybe...'],
        ['', '', '', 'Testing\nTesting'],
        ['', '', '', '', 'Testing\nTesting'],
        ['', '', '', '', '', 'Testing\nTesting'],
        ['', '', '', '', '', 'Testing\nTesting'],
        ['', '', '', '', '', 'Testing\nTesting'],
        ['', '', '', '', 'Testing\nTesting'],
        ['', '', '', 'Testing\nTesting'],
        ['', 'Cost\nA lot....'],
        [],
        [],
        [],
        ['', '', 'Whatever'],
        ['', '', 'Whatever']
    ]
    
    # Build and print the tree
    root = build_tree(data)
    print(str(root))
    return root

def tree_to_typescript_json(node):
    """Convert a TreeNode structure to TypeScript JSON format."""
    def convert_node(node: 'TreeNode') -> Dict[str, Any]:
        result = {"content": node.content}
        
        if node.children:
            choices = {}
            for child in node.children:
                print("Child topic and content: ", child.topic, child.content)
                key = child.topic.lower()

                if key in choices:
                    counter = 1
                    while f"{key}_{counter}" in choices:
                        counter += 1
                    key = f"{key}_{counter}"

                choices[key] = convert_node(child)
                print("Choices: ", choices)
            result["choices"] = choices
            
        return result
    
    return convert_node(node)

def convert_data(data):
    root = build_tree(data)
    return tree_to_typescript_json(root)


from typing import List, Dict, Any
import json

def transform_data(data: List[List[str]]) -> Dict[str, Any]:
    def parse_content(text: str) -> str:
        return text.strip()
    
    def find_children(rows: List[List[str]], parent_depth: int, start_index: int) -> tuple[Dict[str, Any], int]:
        choices = {}
        i = start_index
        
        while i < len(rows):
            row = rows[i]
            
            # Skip empty rows or rows that don't have enough elements
            if not row or len(row) <= parent_depth:
                i += 1
                continue
                
            # Check if this row belongs to current depth
            current_item = row[parent_depth]
            if not current_item.strip():
                i += 1
                continue
                
            # If we find a non-empty item at a lower depth, we're done with this level
            if any(idx < parent_depth for idx, item in enumerate(row) if item.strip()):
                break
                
            # Generate a unique key for this choice
            base_key = current_item.split('\n')[0].lower().replace(' ', '_')
            key = base_key
            counter = 1
            while key in choices:
                key = f"{base_key}{counter}"
                counter += 1
                
            # Create the choice object
            choice = {"content": parse_content(current_item)}
            
            # Look for children
            if len(row) > parent_depth + 1:
                child_choices, new_index = find_children(rows, parent_depth + 1, i)
                if child_choices:
                    choice["choices"] = child_choices
                i = new_index
            else:
                i += 1
                
            choices[key] = choice
            
        return choices, i
    
    # Handle root content
    if not data or not data[0]:
        return {}
        
    root_content = parse_content(data[0][0])
    root = {
        "content": root_content
    }
    
    # Find all child choices
    choices, _ = find_children(data, 1, 1)
    if choices:
        root["choices"] = choices

    
        
    return root


