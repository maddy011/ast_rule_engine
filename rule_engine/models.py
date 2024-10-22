from django.db import models

class Rule(models.Model):
    rule_string = models.TextField()
    ast_representation = models.JSONField()

    def __str__(self):
        return self.rule_string
