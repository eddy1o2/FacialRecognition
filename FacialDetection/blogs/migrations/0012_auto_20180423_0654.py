# Generated by Django 2.0.3 on 2018-04-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0011_auto_20180420_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default='abc.jpg', null=True, upload_to=''),
        ),
    ]
