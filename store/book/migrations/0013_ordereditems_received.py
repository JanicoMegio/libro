# Generated by Django 4.0.3 on 2023-09-12 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0012_order_total_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordereditems',
            name='received',
            field=models.BooleanField(default=False),
        ),
    ]
