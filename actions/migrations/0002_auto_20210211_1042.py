# Generated by Django 3.1.3 on 2021-02-11 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='created',
            field=models.DateTimeField(db_index=True, null=True),
        ),
    ]