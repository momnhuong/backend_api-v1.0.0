# Generated by Django 2.2.10 on 2020-10-13 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_order_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='tax_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
