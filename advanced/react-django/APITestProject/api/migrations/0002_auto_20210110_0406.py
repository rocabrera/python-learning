# Generated by Django 3.1.5 on 2021-01-10 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='descripton',
            new_name='description',
        ),
    ]