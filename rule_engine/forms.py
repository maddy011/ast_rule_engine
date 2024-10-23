from django import forms


class RuleForm(forms.Form):
    rule_string = forms.CharField(
        label="Rule String", max_length=500, widget=forms.Textarea
    )


class CombineRulesForm(forms.Form):
    rule_ids = forms.CharField(
        label="Rule IDs (comma separated)", widget=forms.TextInput
    )


class RuleEvaluateForm(forms.Form):
    rule_id = forms.IntegerField(label="Rule ID")
    data = forms.CharField(label="Data (JSON)", widget=forms.Textarea)


class ModifyRuleForm(forms.Form):
    rule_id = forms.IntegerField(label="Rule ID")
    new_rule_string = forms.CharField(label="New Rule String", widget=forms.Textarea)
