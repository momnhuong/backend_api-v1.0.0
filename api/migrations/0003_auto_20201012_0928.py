# Generated by Django 2.2.10 on 2020-10-12 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201012_0920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
