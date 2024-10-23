from django.db import models
import json


class Rule(models.Model):
    rule_string = models.TextField()
    ast_representation = models.JSONField()

    def __str__(self):
        return self.rule_string


# class Rule(models.Model):
#     rule_string = models.CharField(max_length=255)
#     ast = models.TextField()

#     def __str__(self):
#         return self.rule_string
