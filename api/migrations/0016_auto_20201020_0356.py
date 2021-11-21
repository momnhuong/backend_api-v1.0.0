# Generated by Django 2.2.10 on 2020-10-20 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_productofcustomer_contract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='alert_type',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='content',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='customer_id',
        ),
        migrations.RemoveField(
            model_name='alert',
            name='title',
        ),
        migrations.AddField(
            model_name='alert',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Customer'),
        ),
        migrations.AddField(
            model_name='alert',
            name='message',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='on_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='priority',
            field=models.CharField(choices=[('LOW', 'LOW'), ('NORMAL', 'NORMAL'), ('HIGH', 'HIGH'), ('URGENT', 'URGENT')], default='LOW', max_length=50),
        ),
        migrations.AddField(
            model_name='alert',
            name='product_of_customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ProductOfCustomer'),
        ),
        migrations.AddField(
            model_name='alert',
            name='read',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='alert',
            name='system_id',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
