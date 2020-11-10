# Generated by Django 3.1.2 on 2020-11-11 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('stay', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stay',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.host'),
        ),
        migrations.AddField(
            model_name='stay',
            name='house_rules',
            field=models.ManyToManyField(related_name='stay_houserule', through='stay.StayHouseRule', to='stay.HouseRule'),
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.rentaltype'),
        ),
        migrations.AddField(
            model_name='stay',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.subcategory'),
        ),
        migrations.AddField(
            model_name='room',
            name='stay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.stay'),
        ),
        migrations.AddField(
            model_name='image',
            name='stay',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.stay'),
        ),
    ]