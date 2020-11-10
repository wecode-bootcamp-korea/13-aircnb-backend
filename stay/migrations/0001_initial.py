# Generated by Django 3.1.2 on 2020-11-11 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'amenities',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('names', models.CharField(max_length=50)),
                ('icon_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'facilities',
            },
        ),
        migrations.CreateModel(
            name='HouseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon_url', models.URLField(max_length=2000)),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'house_rules',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'images',
            },
        ),
        migrations.CreateModel(
            name='RentalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('icon_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'rental_types',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('beds', models.IntegerField()),
                ('icon_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='Stay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=60)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=60, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=8)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('description', models.CharField(max_length=2000)),
                ('bathrooms', models.IntegerField()),
                ('capacity', models.IntegerField()),
                ('country', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('address1', models.CharField(max_length=500)),
                ('address2', models.CharField(max_length=500)),
                ('full_address', models.CharField(max_length=1000)),
                ('zipcode', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField()),
            ],
            options={
                'db_table': 'stays',
            },
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.category')),
            ],
            options={
                'db_table': 'subcategories',
            },
        ),
        migrations.CreateModel(
            name='StayHouseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.houserule')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.stay')),
            ],
            options={
                'db_table': 'stay_houserules',
            },
        ),
        migrations.CreateModel(
            name='StayFacility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.facility')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.stay')),
            ],
            options={
                'db_table': 'stay_facilities',
            },
        ),
        migrations.CreateModel(
            name='StayAmenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.amenity')),
                ('stay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stay.stay')),
            ],
            options={
                'db_table': 'stay_amenities',
            },
        ),
        migrations.AddField(
            model_name='stay',
            name='amenities',
            field=models.ManyToManyField(related_name='stay_amenity', through='stay.StayAmenity', to='stay.Amenity'),
        ),
        migrations.AddField(
            model_name='stay',
            name='facilities',
            field=models.ManyToManyField(related_name='stay_facility', through='stay.StayFacility', to='stay.Facility'),
        ),
    ]
