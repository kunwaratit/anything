# Generated by Django 3.2 on 2023-10-02 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EnDecrypt', '0006_alter_encryptedfile_encrypted_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptedfile',
            name='encrypted_file',
            field=models.FileField(max_length=255, upload_to='encrypted_files/'),
        ),
    ]
