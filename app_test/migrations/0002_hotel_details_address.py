# Generated by Django 3.2.8 on 2021-10-18 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel_details',
            name='Address',
            field=models.CharField(default=0, max_length=254),
            preserve_default=False,
        ),
    ]