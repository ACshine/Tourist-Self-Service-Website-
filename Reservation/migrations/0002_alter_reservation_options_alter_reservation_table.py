# Generated by Django 5.0.6 on 2024-07-09 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reservation',
            options={'ordering': ['rv_date'], 'verbose_name': '预约', 'verbose_name_plural': '预约'},
        ),
        migrations.AlterModelTable(
            name='reservation',
            table='reservation',
        ),
    ]
