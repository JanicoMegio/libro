# Generated by Django 4.0.3 on 2023-09-13 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0016_remove_ordereditems_review_order_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerreview',
            name='item_review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.order'),
        ),
    ]
