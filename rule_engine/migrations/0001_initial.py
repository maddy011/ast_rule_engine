# Generated by Django 4.2 on 2024-10-23 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule_string', models.TextField()),
                ('ast_representation', models.JSONField()),
            ],
        ),
    ]