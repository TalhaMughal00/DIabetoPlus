# Generated by Django 5.1 on 2024-09-06 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='predictions',
            old_name='HbA1c_level',
            new_name='hba1c_level',
        ),
    ]
