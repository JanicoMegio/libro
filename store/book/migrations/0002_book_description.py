# Generated by Django 4.2.4 on 2023-08-23 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]