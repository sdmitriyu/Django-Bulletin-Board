# Generated by Django 5.0.3 on 2025-01-10 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='images2/'),
        ),
    ]
