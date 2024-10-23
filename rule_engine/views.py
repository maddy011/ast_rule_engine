from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rule
from .services.rule_parser import (
    ASTNode,
    parse_rule_string,
    combine_rule_logic,
    evaluate_rule_logic,
    modify_rule_logic,
)
import json
import logging

logging.basicConfig(level=logging.DEBUG)


from django.shortcuts import render, redirect
from .forms import RuleForm, CombineRulesForm, RuleEvaluateForm, ModifyRuleForm
import json


def create_rule(request):
    if request.method == "POST":
        form = RuleForm(request.POST)
        if form.is_valid():
            rule_string = form.cleaned_data["rule_string"]
            ast = parse_rule_string(rule_string)
            rule = Rule(
                rule_string=rule_string, ast_representation=json.dumps(ast.to_dict())
            )
            rule.save()
            return redirect("create_rule")  # Redirect to the same page after saving
    else:
        form = RuleForm()

    return render(request, "rule_engine/create_rule.html", {"form": form})


# @csrf_exempt
# def combine_rules(request):
#     if request.method == "POST":
#         rule_ids = json.loads(request.body)["rule_ids"]
#         rules = Rule.objects.filter(id__in=rule_ids)
#         combined_ast = ASTNode(
#             "operator",
#             "AND",
#             *[ASTNode.from_dict(json.loads(rule.ast)) for rule in rules],
#         )
#         combined_rule_string = " AND ".join([rule.rule_string for rule in rules])
#         combined_rule = Rule(
#             rule_string=combined_rule_string, ast=json.dumps(combined_ast.to_dict())
#         )
#         combined_rule.save()
#         return JsonResponse(
#             {"id": combined_rule.id, "combined_ast": json.dumps(combined_ast.to_dict())}
#         )


# @csrf_exempt
# def combine_rules(request):
#     if request.method == "POST":
#         rule_ids = json.loads(request.body)["rule_ids"]
#         combined_rule, combined_ast = combine_rule_logic(rule_ids)
#         return JsonResponse(
#             {"id": combined_rule.id, "combined_ast": json.dumps(combined_ast.to_dict())}
#         )
#     return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
def combine_rules(request):
    if request.method == "POST":
        form = CombineRulesForm(request.POST)
        if form.is_valid():
            rule_ids = list(
                map(int, form.cleaned_data["rule_ids"].split(","))
            )  # Convert input to a list of integers
            combined_rule, combined_ast = combine_rule_logic(rule_ids)
            return JsonResponse(
                {
                    "id": combined_rule.id,
                    "combined_ast": json.dumps(combined_ast.to_dict()),
                }
            )
    else:
        form = CombineRulesForm()

    return render(request, "rule_engine/combine_rules.html", {"form": form})


# @csrf_exempt
# def evaluate_rule(request):
#     if request.method == "POST":
#         rule_id = json.loads(request.body)["rule_id"]
#         rule = Rule.objects.filter(id=rule_id).first()
#         if not rule:
#             return JsonResponse({"error": "Rule not found"}, status=404)
#         ast = ASTNode.from_dict(json.loads(rule.ast))
#         data = json.loads(request.body)["data"]
#         result = evaluate_ast(ast, data)
#         return JsonResponse({"result": result})


def evaluate_rule(request):
    if request.method == "POST":
        form = RuleEvaluateForm(request.POST)
        if form.is_valid():
            rule_id = form.cleaned_data["rule_id"]
            print("rule id", rule_id)

            # Check if "data" is not empty or invalid
            try:
                print("within try")
                data = json.loads(form.cleaned_data["data"])
                print("dataa", data)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data"}, status=400)

            result, error = evaluate_rule_logic(rule_id, data)
            if error:
                return JsonResponse({"error": error}, status=404)
            return JsonResponse({"result": result})
    else:
        form = RuleEvaluateForm()

    return render(request, "rule_engine/evaluate_rule.html", {"form": form})


# @csrf_exempt
# def modify_rule(request):
#     if request.method == "POST":
#         try:
#             rule_id = json.loads(request.body)["rule_id"]
#             new_rule_string = json.loads(request.body)["new_rule_string"]
#             rule = Rule.objects.filter(id=rule_id).first()
#             if rule:
#                 rule.rule_string = new_rule_string
#                 rule.ast = json.dumps(parse_rule_string(new_rule_string).to_dict())
#                 rule.save()
#                 return JsonResponse({"message": "Rule updated successfully"})
#             else:
#                 return JsonResponse({"message": "Rule not found"}, status=404)
#         except Exception as e:
#             logging.error(f"Error modifying rule: {e}")
#             return JsonResponse({"error": "Internal Server Error"}, status=500)


def modify_rule(request):
    if request.method == "POST":
        form = ModifyRuleForm(request.POST)
        if form.is_valid():
            rule_id = form.cleaned_data["rule_id"]
            new_rule_string = form.cleaned_data["new_rule_string"]

            rule, error = modify_rule_logic(rule_id, new_rule_string)
            if error:
                return JsonResponse({"message": error}, status=404)

            return JsonResponse({"message": "Rule updated successfully"})
    else:
        form = ModifyRuleForm()

    return render(request, "rule_engine/modify_rule.html", {"form": form})
