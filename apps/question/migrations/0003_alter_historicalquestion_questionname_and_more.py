# Generated by Django 4.1.6 on 2023-09-05 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0002_alter_historicalquestion_questionname_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalquestion",
            name="questionname",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="question",
            name="questionname",
            field=models.TextField(),
        ),
    ]
