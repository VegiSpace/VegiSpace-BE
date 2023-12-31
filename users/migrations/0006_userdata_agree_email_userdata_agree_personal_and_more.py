# Generated by Django 4.1 on 2023-11-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_userdata_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='agree_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='agree_personal',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='agree_sms',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userdata',
            name='agree_terms',
            field=models.BooleanField(default=True),
        ),
    ]
