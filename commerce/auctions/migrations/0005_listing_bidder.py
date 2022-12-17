# Generated by Django 4.1.3 on 2022-12-10 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bidder',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='my_biddings', to=settings.AUTH_USER_MODEL),
        ),
    ]
