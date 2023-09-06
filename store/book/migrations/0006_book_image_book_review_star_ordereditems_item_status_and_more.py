# Generated by Django 4.0.3 on 2023-09-02 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('book', '0005_remove_ordereditems_order_ordereditems_buy_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(default=1, upload_to='book_images'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='review_star',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='item_status',
            field=models.CharField(choices=[('pending', 'PENDING'), ('order confirm', 'ORDER CONFIRM'), ('out of delivery', 'OUT OF DELIVERY'), ('delivered', 'DELIVERED')], default='pending', max_length=20),
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address1', models.TextField(max_length=1000)),
                ('address2', models.TextField(blank=True, max_length=1000, null=True)),
                ('fname', models.CharField(max_length=255)),
                ('lname', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('contact', models.CharField(max_length=11)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=5000)),
                ('star', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('item_review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.ordereditems')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
