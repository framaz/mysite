# Generated by Django 2.1.5 on 2019-02-25 10:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0009_message_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 25, 10, 30, 15, 189150, tzinfo=utc), verbose_name='date published'),
        ),
    ]
