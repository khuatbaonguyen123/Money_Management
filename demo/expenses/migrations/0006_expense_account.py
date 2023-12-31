# Generated by Django 4.2.7 on 2023-11-26 04:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_delete_profile'),
        ('expenses', '0005_remove_expense_categoryid_alter_expense_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='account',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
    ]
