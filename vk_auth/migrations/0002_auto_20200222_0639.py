# Generated by Django 2.2.10 on 2020-02-22 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vk_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('user_id', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('access_token', models.CharField(max_length=200)),
                ('expires_at', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='OAuth2Token',
        ),
    ]
