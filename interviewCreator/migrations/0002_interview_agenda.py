# Generated by Django 3.1 on 2020-08-29 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interviewCreator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='agenda',
            field=models.CharField(default='Mock Interview', max_length=50),
            preserve_default=False,
        ),
    ]