# Generated by Django 5.0.2 on 2025-02-25 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likelion', '0003_author_remove_tweet_author_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='username',
            new_name='author_id',
        ),
    ]
