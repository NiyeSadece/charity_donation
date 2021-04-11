# Generated by Django 3.2 on 2021-04-10 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('type', models.IntegerField(choices=[(1, 'fundacja'), (2, 'organizacja pozarządowa'), (3, 'zbiórka lokalna')], default='1')),
                ('categories', models.ManyToManyField(to='donation_page.Category')),
            ],
        ),
    ]