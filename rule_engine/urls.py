from django.urls import path
from .views import create_rule, combine_rules, evaluate_rule, modify_rule

urlpatterns = [
    path("create_rule/", create_rule, name="create_rule"),
    path("combine_rules/", combine_rules, name="combine_rules"),
    path("evaluate_rule/", evaluate_rule, name="evaluate_rule"),
    path("modify_rule/", modify_rule, name="modify_rule"),
]
