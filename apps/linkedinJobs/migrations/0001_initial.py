# Generated by Django 4.1.3 on 2023-08-04 22:59

from django.db import migrations, models
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLinkedinJobs',
            fields=[
                ('id', models.IntegerField(blank=True, db_index=True)),
                ('state', models.BooleanField(default=True, verbose_name='State')),
                ('created_date', models.DateField(blank=True, editable=False, verbose_name='Created Date')),
                ('modified_date', models.DateField(blank=True, editable=False, verbose_name='Update Date')),
                ('deleted_date', models.DateField(blank=True, editable=False, verbose_name='Deleted Date')),
                ('jobName', models.CharField(max_length=100)),
                ('jobDescription', models.TextField()),
                ('jobUrl', models.TextField()),
                ('posibilityPercentage', models.IntegerField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
            ],
            options={
                'verbose_name': 'historical LinkedinJob',
                'verbose_name_plural': 'historical LinkedinJobs',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='LinkedinJobs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='State')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='Created Date')),
                ('modified_date', models.DateField(auto_now=True, verbose_name='Update Date')),
                ('deleted_date', models.DateField(auto_now=True, verbose_name='Deleted Date')),
                ('jobName', models.CharField(max_length=100)),
                ('jobDescription', models.TextField()),
                ('jobUrl', models.TextField()),
                ('posibilityPercentage', models.IntegerField()),
            ],
            options={
                'verbose_name': 'LinkedinJob',
                'verbose_name_plural': 'LinkedinJobs',
            },
        ),
    ]
