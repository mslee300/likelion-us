# Generated by Django 5.0.2 on 2025-02-25 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likelion', '0008_alter_author_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_id',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
