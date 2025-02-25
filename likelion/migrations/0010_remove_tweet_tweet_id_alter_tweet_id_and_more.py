# Generated by Django 5.0.2 on 2025-02-25 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likelion', '0009_alter_tweet_tweet_id_alter_tweet_tweet_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='tweet_id',
        ),
        migrations.AlterField(
            model_name='tweet',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tweet',
            name='tweet_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
