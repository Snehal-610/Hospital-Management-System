# Generated by Django 3.2.4 on 2021-07-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0005_rename_user_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='DStatus',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approve', 'Approve'), ('Reject', 'Reject')], default='Pending', max_length=100),
        ),
    ]