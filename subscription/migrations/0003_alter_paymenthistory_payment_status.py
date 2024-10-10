# Generated by Django 5.1.1 on 2024-10-09 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_alter_paymenthistory_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='payment_status',
            field=models.CharField(choices=[('f', 'Failed'), ('s', 'Success'), ('p', 'Pending')], max_length=1),
        ),
    ]
