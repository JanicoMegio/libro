# Generated by Django 4.0.3 on 2023-09-07 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0006_book_image_book_review_star_ordereditems_item_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='birthdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='published',
            field=models.DateField(null=True),
        ),
    ]