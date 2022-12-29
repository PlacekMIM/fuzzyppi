# Generated by Django 3.0.5 on 2021-07-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuzzy_score', '0003_auto_20200430_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ppiscore',
            name='protein1',
            field=models.CharField(max_length=20, verbose_name='Protein 1'),
        ),
        migrations.AlterField(
            model_name='ppiscore',
            name='protein2',
            field=models.CharField(max_length=20, verbose_name='Protein 1'),
        ),
        migrations.AlterField(
            model_name='ppiscore',
            name='score',
            field=models.DecimalField(decimal_places=6, max_digits=7, verbose_name='Fuzzy PPI score '),
        ),
    ]