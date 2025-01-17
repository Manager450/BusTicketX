# Generated by Django 5.0.6 on 2024-07-17 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_passenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('departure_time', models.TimeField()),
                ('arrival_time', models.TimeField()),
                ('available_seats', models.IntegerField()),
                ('fare', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.bus')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.route')),
            ],
        ),
    ]
