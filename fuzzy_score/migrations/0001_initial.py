# Generated by Django 3.0.5 on 2020-04-13 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PPIScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protein1', models.CharField(max_length=20, verbose_name='protein code 1')),
                ('protein2', models.CharField(max_length=20, verbose_name='protein code 1')),
                ('score', models.DecimalField(decimal_places=4, max_digits=5, verbose_name='fuzzy ppi score ')),
            ],
        ),
    ]
