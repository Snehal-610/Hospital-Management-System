# Generated by Django 3.2.4 on 2021-07-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reception', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='EmailId',
            new_name='Email',
        ),
        migrations.AddField(
            model_name='user',
            name='OTP',
            field=models.CharField(max_length=6, null=True),
        ),
    ]
