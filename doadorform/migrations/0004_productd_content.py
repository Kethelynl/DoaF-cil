# Generated by Django 5.1.7 on 2025-03-29 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doadorform', '0003_rename_quantidade_productd_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='productd',
            name='content',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
