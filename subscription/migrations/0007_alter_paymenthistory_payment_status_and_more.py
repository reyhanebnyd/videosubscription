# Generated by Django 5.1.1 on 2024-10-12 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_alter_paymenthistory_payment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_status',
            field=models.CharField(choices=[('s', 'Success'), ('f', 'Failed'), ('p', 'Pending')], max_length=1),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='interval',
            field=models.CharField(choices=[('y', 'yearly'), ('s', '3 Month'), ('m', 'Monthly'), ('h', '6 Month')], max_length=1),
        ),
    ]
