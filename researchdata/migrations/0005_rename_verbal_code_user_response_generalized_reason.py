# Generated by Django 5.0.6 on 2024-06-27 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researchdata', '0004_variable_range_user_response_delete_response'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_response',
            old_name='verbal_code',
            new_name='generalized_reason',
        ),
    ]
