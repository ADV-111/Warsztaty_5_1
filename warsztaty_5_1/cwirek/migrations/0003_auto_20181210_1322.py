# Generated by Django 2.1.1 on 2018-12-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cwirek', '0002_comments_messages_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messages',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tweet',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]
