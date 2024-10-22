from django.urls import path
from .views import CreateRuleView, EvaluateRuleView

urlpatterns = [
    path('create_rule/', CreateRuleView.as_view(), name='create_rule'),
    path('evaluate_rule/', EvaluateRuleView.as_view(), name='evaluate_rule'),
]
