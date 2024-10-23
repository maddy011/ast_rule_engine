import re


class ASTNode:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None,
        }

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None
        return cls(
            type=data["type"],
            value=data["value"],
            left=cls.from_dict(data["left"]),
            right=cls.from_dict(data["right"]),
        )


def parse_rule_string(rule_string):
    tokens = rule_string.replace("(", " ( ").replace(")", " ) ").split()

    def parse_expression():
        stack = [[]]
        for token in tokens:
            if token == "(":
                stack.append([])
            elif token == ")":
                expr = stack.pop()
                stack[-1].append(expr)
            elif token in ["AND", "OR"]:
                stack[-1].append(token)
            else:
                stack[-1].append(token)

        def build_tree(expr):
            if isinstance(expr, list):
                if len(expr) == 1:
                    return build_tree(expr[0])
                elif "OR" in expr:
                    idx = expr.index("OR")
                    return ASTNode(
                        "operator",
                        "OR",
                        build_tree(expr[:idx]),
                        build_tree(expr[idx + 1 :]),
                    )
                elif "AND" in expr:
                    idx = expr.index("AND")
                    return ASTNode(
                        "operator",
                        "AND",
                        build_tree(expr[:idx]),
                        build_tree(expr[idx + 1 :]),
                    )
            return ASTNode("operand", " ".join(expr))

        return build_tree(stack[0])

    return parse_expression()


def evaluate_ast(ast, data):
    if ast.type == "operator":
        if ast.value == "AND":
            return evaluate_ast(ast.left, data) and evaluate_ast(ast.right, data)
        elif ast.value == "OR":
            return evaluate_ast(ast.left, data) or evaluate_ast(ast.right, data)
    elif ast.type == "operand":
        left, op, right = ast.value.split()
        left_value = data.get(left)
        right_value = int(right) if right.isdigit() else right.strip("'")
        if op == ">":
            return left_value > right_value
        elif op == "<":
            return left_value < right_value
        elif op == "=":
            return left_value == right_value
    return False


# def create_rule(rule_string):
#     tokens = re.findall(r"\w+|[><=]+|'[^']+'|AND|OR|\(|\)", rule_string)

#     def parse_expression(tokens):
#         stack = []
#         for token in tokens:
#             if token in ["AND", "OR"]:
#                 right = stack.pop()
#                 left = stack.pop()
#                 stack.append(ASTNode(node_type="operator", left=left, right=right, value=token))
#             elif re.match(r"'[^']+'|\d+", token):
#                 stack.append(ASTNode(node_type="operand", value=token))
#             else:
#                 stack.append(ASTNode(node_type="operand", value=token))
#         return stack[0]  # Final AST

#     return parse_expression(tokens)


# def combine_rules(rules, operator="AND"):
#     root = None
#     for rule in rules:
#         if root is None:
#             root = rule
#         else:
#             root = ASTNode(node_type="operator", left=root, right=rule, value=operator)
#     return root


# def evaluate_rule(ast_node, data):
#     if ast_node.node_type == "operator":
#         if ast_node.value == "AND":
#             return evaluate_rule(ast_node.left, data) and evaluate_rule(ast_node.right, data)
#         elif ast_node.value == "OR":
#             return evaluate_rule(ast_node.left, data) or evaluate_rule(ast_node.right, data)
#     elif ast_node.node_type == "operand":
#         attr, op, val = ast_node.value.split()
#         attr_val = data.get(attr)
#         if op == ">":
#             return attr_val > int(val)
#         elif op == "<":
#             return attr_val < int(val)
#         elif op == "=":
#             return attr_val == val.strip("'")
#     return False
