# Generated by Django 4.2.7 on 2023-11-25 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_initialamount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='type',
            field=models.CharField(choices=[(1, 'Cash'), (2, 'Bank Accounts'), (3, 'Cards')], max_length=255, null=True),
        ),
    ]