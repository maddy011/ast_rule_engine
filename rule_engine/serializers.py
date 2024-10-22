from rest_framework import serializers

class RuleSerializer(serializers.Serializer):
    rule_string = serializers.CharField()
