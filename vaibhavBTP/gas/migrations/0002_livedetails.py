# Generated by Django 3.0.8 on 2020-12-07 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('gas', models.CharField(max_length=50)),
                ('value', models.FloatField()),
            ],
        ),
    ]
