# Generated by Django 3.2 on 2023-09-22 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_usersession'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usersession',
            options={'ordering': ['-login_time']},
        ),
        migrations.RenameField(
            model_name='usersession',
            old_name='created_at',
            new_name='login_time',
        ),
    ]
