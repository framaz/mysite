# Generated by Django 2.1.5 on 2019-02-05 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.CharField(max_length=9)),
                ('is_ended', models.BooleanField(default=False)),
                ('hoster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hoster_of_ticgame', to=settings.AUTH_USER_MODEL)),
                ('o_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_y_of_ticgame', to=settings.AUTH_USER_MODEL)),
                ('x_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_x_of_ticgame', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]