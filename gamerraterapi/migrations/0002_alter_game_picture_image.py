# Generated by Django 3.2.1 on 2021-05-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamerraterapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game_picture',
            name='image',
            field=models.ImageField(null=True, upload_to='actionimages'),
        ),
    ]
