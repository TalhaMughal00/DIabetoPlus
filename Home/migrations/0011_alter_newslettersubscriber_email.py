# Generated by Django 4.2.15 on 2024-10-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_newslettersubscriber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newslettersubscriber',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
