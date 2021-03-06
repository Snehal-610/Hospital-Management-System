# Generated by Django 3.2.4 on 2021-07-04 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Patients', '0008_alter_appointments_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='Age',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='patients',
            name='Lname',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='patients',
            name='Phone_Number',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='patients',
            name='Role',
            field=models.CharField(default='Patient', max_length=50),
        ),
    ]
