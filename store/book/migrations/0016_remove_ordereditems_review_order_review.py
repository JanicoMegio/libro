# Generated by Django 4.0.3 on 2023-09-13 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_alter_customerreview_item_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordereditems',
            name='review',
        ),
        migrations.AddField(
            model_name='order',
            name='review',
            field=models.BooleanField(default=False),
        ),
    ]
