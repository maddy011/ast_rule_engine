import re


class ASTNode:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  
        self.left = left
        self.right = right
        self.value = value  

    def __repr__(self):
        if self.node_type == "operator":
            return f"({self.left} {self.value} {self.right})"
        return str(self.value)


def create_rule(rule_string):
    tokens = re.findall(r"\w+|[><=]+|'[^']+'|AND|OR|\(|\)", rule_string)
    
    def parse_expression(tokens):
        stack = []
        for token in tokens:
            if token in ["AND", "OR"]:
                right = stack.pop()
                left = stack.pop()
                stack.append(ASTNode(node_type="operator", left=left, right=right, value=token))
            elif re.match(r"'[^']+'|\d+", token):
                stack.append(ASTNode(node_type="operand", value=token))
            else:
                stack.append(ASTNode(node_type="operand", value=token))
        return stack[0]  # Final AST
    
    return parse_expression(tokens)


def combine_rules(rules, operator="AND"):
    root = None
    for rule in rules:
        if root is None:
            root = rule
        else:
            root = ASTNode(node_type="operator", left=root, right=rule, value=operator)
    return root


def evaluate_rule(ast_node, data):
    if ast_node.node_type == "operator":
        if ast_node.value == "AND":
            return evaluate_rule(ast_node.left, data) and evaluate_rule(ast_node.right, data)
        elif ast_node.value == "OR":
            return evaluate_rule(ast_node.left, data) or evaluate_rule(ast_node.right, data)
    elif ast_node.node_type == "operand":
        attr, op, val = ast_node.value.split()
        attr_val = data.get(attr)
        if op == ">":
            return attr_val > int(val)
        elif op == "<":
            return attr_val < int(val)
        elif op == "=":
            return attr_val == val.strip("'")
    return False