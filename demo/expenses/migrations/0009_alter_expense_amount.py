# Generated by Django 4.2.7 on 2023-11-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_alter_expense_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
