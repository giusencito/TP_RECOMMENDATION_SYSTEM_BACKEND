# Generated by Django 4.1.3 on 2023-09-15 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='resultTest',
        ),
        migrations.RemoveField(
            model_name='historicalfeedback',
            name='resultTest',
        ),
        migrations.AddField(
            model_name='feedback',
            name='token_link',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='historicalfeedback',
            name='token_link',
            field=models.CharField(blank=True, db_index=True, max_length=50, null=True),
        ),
    ]