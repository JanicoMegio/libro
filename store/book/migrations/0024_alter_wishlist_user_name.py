# Generated by Django 4.0.3 on 2023-09-22 14:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0023_remove_wishlist_wish_book_wishlist_wish_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='user_name',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
