# Generated by Django 4.1.2 on 2022-11-19 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200, unique=True)),
                ('name', models.CharField(default='User', max_length=255)),
                ('red_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-red_date',),
            },
        ),
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.TextField(default='Newsletter from Graphico')),
                ('body', models.TextField()),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
