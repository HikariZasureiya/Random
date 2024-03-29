# Generated by Django 5.0 on 2023-12-15 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_messaging_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='pfp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=15)),
                ('profilepic', models.ImageField(upload_to='profilepics')),
            ],
        ),
    ]
