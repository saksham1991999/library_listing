# Generated by Django 2.2 on 2020-05-19 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200520_0442'),
    ]

    operations = [
        migrations.AddField(
            model_name='enquiry',
            name='remarks',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
