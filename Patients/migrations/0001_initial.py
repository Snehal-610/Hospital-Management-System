# Generated by Django 3.2.4 on 2021-07-01 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Reception', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Fname', models.CharField(max_length=50)),
                ('Lname', models.CharField(max_length=50, null=True)),
                ('Age', models.PositiveIntegerField(null=True)),
                ('Role', models.CharField(default='Patient', max_length=50, null=True)),
                ('Symptoms', models.CharField(max_length=100)),
                ('Address', models.CharField(max_length=300, null=True)),
                ('Phone_Number', models.CharField(max_length=12, null=True, unique=True)),
                ('Gender', models.CharField(choices=[('Gender', 'Gender'), ('Male', 'Male'), ('Female', 'Female')], default='Gender', max_length=6)),
                ('Email', models.EmailField(max_length=100, unique=True)),
                ('Password', models.CharField(max_length=100)),
                ('Created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Aprove', 'Aprove'), ('Reject', 'Reject')], default='Pending', max_length=30, null=True)),
                ('User', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Reception.user')),
            ],
        ),
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AppointmentDate', models.DateField(auto_now=True)),
                ('Description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False)),
                ('PatientId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Patients.patients')),
            ],
        ),
    ]
