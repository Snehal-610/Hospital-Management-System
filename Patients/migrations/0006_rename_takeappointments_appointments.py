# Generated by Django 3.2.4 on 2021-07-01 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
        ('Patients', '0005_rename_doctorsid_takeappointments_doctorid'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TakeAppointments',
            new_name='Appointments',
        ),
    ]