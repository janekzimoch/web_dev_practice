# Generated by Django 4.1.3 on 2023-02-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time_published',
            field=models.CharField(default='2015-10-15 07:49:18', max_length=32),
            preserve_default=False,
        ),
    ]
