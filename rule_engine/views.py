from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RuleSerializer
from .services.rule_parser import create_rule, evaluate_rule

class CreateRuleView(APIView):
    def post(self, request):
        serializer = RuleSerializer(data=request.data)
        if serializer.is_valid():
            rule_string = serializer.validated_data['rule_string']
            ast = create_rule(rule_string)  # Parse into AST
            # Optionally save the rule in DB or return the AST
            return Response({"ast": ast}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvaluateRuleView(APIView):
    def post(self, request):
        ast = request.data.get('ast')  # Get the AST from request body
        data = request.data.get('data')  # Get user data
        result = evaluate_rule(ast, data)  # Evaluate the rule
        return Response({"result": result}, status=status.HTTP_200_OK)
