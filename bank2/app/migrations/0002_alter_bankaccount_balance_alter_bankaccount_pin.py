# Generated by Django 5.1.3 on 2024-12-28 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='balance',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='pin',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
