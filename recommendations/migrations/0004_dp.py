# Generated by Django 4.2.15 on 2024-10-08 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recommendations', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakfast_plan', models.JSONField()),
                ('lunch_plan', models.JSONField()),
                ('dinner_plan', models.JSONField()),
                ('bmr', models.FloatField()),
                ('bmi', models.FloatField()),
                ('diet_type', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
