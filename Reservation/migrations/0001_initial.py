# Generated by Django 5.0.6 on 2024-07-09 04:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Rt_Rq', '0001_initial'),
        ('Tourist', '0004_alter_tourist_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rv_date', models.DateField()),
                ('status', models.BooleanField()),
                ('rt_rq_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='Rt_Rq.rt_rq')),
                ('tr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='Tourist.tourist')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
                'ordering': ['rv_date'],
            },
        ),
    ]
