# Generated by Django 5.0 on 2023-12-16 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsystem', '0002_pim_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pim',
            name='profilepic',
            field=models.ImageField(null=True, upload_to='profilepics/'),
        ),
    ]
