# Generated by Django 3.2 on 2023-10-02 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnDecrypt', '0005_alter_encryptedfile_encrypted_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptedfile',
            name='encrypted_file',
            field=models.FileField(upload_to='encrypted_files/'),
        ),
    ]
