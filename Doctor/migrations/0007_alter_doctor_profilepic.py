# Generated by Django 3.2.4 on 2021-07-13 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0006_alter_doctor_dstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='ProfilePic',
            field=models.FileField(default='none.jpg', upload_to='assets/images/doctors'),
        ),
    ]