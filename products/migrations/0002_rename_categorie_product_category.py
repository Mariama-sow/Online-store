# Generated by Django 5.1.5 on 2025-03-15 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categorie',
            new_name='Category',
        ),
    ]
