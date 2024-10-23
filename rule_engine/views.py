from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rule
from .services.rule_parser import ASTNode, parse_rule_string, evaluate_ast
import json
import logging

logging.basicConfig(level=logging.DEBUG)


@csrf_exempt
def create_rule(request):
    if request.method == "POST":
        rule_string = json.loads(request.body)["rule_string"]
        ast = parse_rule_string(rule_string)
        rule = Rule(rule_string=rule_string, ast=json.dumps(ast.to_dict()))
        rule.save()
        return JsonResponse({"id": rule.id, "ast": rule.ast})


@csrf_exempt
def combine_rules(request):
    if request.method == "POST":
        rule_ids = json.loads(request.body)["rule_ids"]
        rules = Rule.objects.filter(id__in=rule_ids)
        combined_ast = ASTNode(
            "operator",
            "AND",
            *[ASTNode.from_dict(json.loads(rule.ast)) for rule in rules],
        )
        combined_rule_string = " AND ".join([rule.rule_string for rule in rules])
        combined_rule = Rule(
            rule_string=combined_rule_string, ast=json.dumps(combined_ast.to_dict())
        )
        combined_rule.save()
        return JsonResponse(
            {"id": combined_rule.id, "combined_ast": json.dumps(combined_ast.to_dict())}
        )


@csrf_exempt
def evaluate_rule(request):
    if request.method == "POST":
        rule_id = json.loads(request.body)["rule_id"]
        rule = Rule.objects.filter(id=rule_id).first()
        if not rule:
            return JsonResponse({"error": "Rule not found"}, status=404)
        ast = ASTNode.from_dict(json.loads(rule.ast))
        data = json.loads(request.body)["data"]
        result = evaluate_ast(ast, data)
        return JsonResponse({"result": result})


@csrf_exempt
def modify_rule(request):
    if request.method == "POST":
        try:
            rule_id = json.loads(request.body)["rule_id"]
            new_rule_string = json.loads(request.body)["new_rule_string"]
            rule = Rule.objects.filter(id=rule_id).first()
            if rule:
                rule.rule_string = new_rule_string
                rule.ast = json.dumps(parse_rule_string(new_rule_string).to_dict())
                rule.save()
                return JsonResponse({"message": "Rule updated successfully"})
            else:
                return JsonResponse({"message": "Rule not found"}, status=404)
        except Exception as e:
            logging.error(f"Error modifying rule: {e}")
            return JsonResponse({"error": "Internal Server Error"}, status=500)


# class CreateRuleView(APIView):
#     def post(self, request):
#         serializer = RuleSerializer(data=request.data)
#         if serializer.is_valid():
#             rule_string = serializer.validated_data['rule_string']
#             ast = create_rule(rule_string)  # Parse into AST
#             # Optionally save the rule in DB or return the AST
#             return Response({"ast": ast}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class EvaluateRuleView(APIView):
#     def post(self, request):
#         ast = request.data.get('ast')  # Get the AST from request body
#         data = request.data.get('data')  # Get user data
#         result = evaluate_rule(ast, data)  # Evaluate the rule
#         return Response({"result": result}, status=status.HTTP_200_OK)
