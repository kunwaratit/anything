# Generated by Django 4.2.3 on 2023-10-01 16:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('EnDecrypt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encryptedfile',
            name='encrypted_file_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
