# Generated by Django 5.0.1 on 2024-02-23 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_transaction_done_no_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='no_user',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
