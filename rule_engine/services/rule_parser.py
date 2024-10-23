import re
import json
from ..models import Rule


class ASTNode:
    def __init__(self, type, value, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": (
                self.left.to_dict() if isinstance(self.left, ASTNode) else self.left
            ),
            "right": (
                self.right.to_dict() if isinstance(self.right, ASTNode) else self.right
            ),
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


def combine_rule_logic(rule_ids):
    rules = Rule.objects.filter(id__in=rule_ids)
    combined_ast = ASTNode(
        "operator",
        "AND",
        *[ASTNode.from_dict(json.loads(rule.ast_representation)) for rule in rules],
    )
    combined_rule_string = " AND ".join([rule.rule_string for rule in rules])
    combined_rule = Rule(
        rule_string=combined_rule_string,
        ast_representation=json.dumps(combined_ast.to_dict()),
    )
    combined_rule.save()
    return combined_rule, combined_ast


# def evaluate_ast(ast, data):
#     if ast.type == "operator":
#         if ast.value == "AND":
#             return evaluate_ast(ast.left, data) and evaluate_ast(ast.right, data)
#         elif ast.value == "OR":
#             return evaluate_ast(ast.left, data) or evaluate_ast(ast.right, data)
#     elif ast.type == "operand":
#         left, op, right = ast.value.split()
#         left_value = data.get(left)
#         right_value = int(right) if right.isdigit() else right.strip("'")
#         if op == ">":
#             return left_value > right_value
#         elif op == "<":
#             return left_value < right_value
#         elif op == "=":
#             return left_value == right_value
#     return False


def evaluate_rule_logic(rule_id, data):
    rule = Rule.objects.filter(id=rule_id).first()
    if not rule:
        return None, "Rule not found"

    ast = ASTNode.from_dict(json.loads(rule.ast_representation))

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

    result = evaluate_ast(ast, data)
    return result, None


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


def modify_rule_logic(rule_id, new_rule_string):
    rule = Rule.objects.filter(id=rule_id).first()
    if not rule:
        return None, "Rule not found"

    rule.rule_string = new_rule_string
    rule.ast_representation = json.dumps(parse_rule_string(new_rule_string).to_dict())
    rule.save()
    return rule, None
