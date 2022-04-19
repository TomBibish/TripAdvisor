# Generated by Django 4.0.2 on 2022-02-09 08:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('price_range', models.CharField(max_length=3)),
                ('image', models.URLField(default='')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.country')),
            ],
        ),
        migrations.CreateModel(
            name='RestaurantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.URLField(default='')),
                ('birth_date', models.DateField()),
                ('address', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.country')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars', models.CharField(choices=[('1', '1 STARS'), ('2', '2 STARS'), ('3', '3 STARS'), ('4', '4 STARS'), ('5', '5 STARS')], max_length=1)),
                ('review_title', models.CharField(max_length=128)),
                ('review_text', models.CharField(blank=True, max_length=528, null=True)),
                ('visit_date', models.DateField()),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.restaurant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='trip_app.restauranttype'),
        ),
    ]