# Generated by Django 4.1.3 on 2022-12-10 10:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_bidder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_biddings', to=settings.AUTH_USER_MODEL),
        ),
    ]