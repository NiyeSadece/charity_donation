# Generated by Django 3.2 on 2021-04-11 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation_page', '0003_donation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterField(
            model_name='donation',
            name='pick_up_comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
