# Generated by Django 2.1.5 on 2019-02-25 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0005_ticket_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='deleted',
            field=models.BooleanField(default='False'),
        ),
    ]
