# Generated by Django 2.2.10 on 2020-10-19 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20201019_0258'),
    ]

    operations = [
        migrations.AddField(
            model_name='productofcustomer',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Contract'),
        ),
    ]
