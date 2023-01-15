# Generated by Django 4.1.3 on 2022-12-19 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_bidder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=256)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings_categories', to='auctions.listing')),
            ],
        ),
    ]