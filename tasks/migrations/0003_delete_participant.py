# Generated by Django 5.1.5 on 2025-02-05 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_event_participants_alter_participant_events'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Participant',
        ),
    ]
