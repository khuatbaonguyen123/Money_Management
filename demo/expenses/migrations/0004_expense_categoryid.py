# Generated by Django 4.2.7 on 2023-11-22 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_alter_expense_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='categoryId',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='expenses.category'),
        ),
    ]
