# Generated by Django 5.1.1 on 2024-10-10 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_remove_chatids_chat_ids_chatids_chats'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatids',
            name='message',
            field=models.TextField(default='', max_length=2048),
        ),
    ]