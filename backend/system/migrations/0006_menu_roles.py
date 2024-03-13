# Generated by Django 4.2 on 2024-03-11 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_menu_component_path_menu_is_catalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='roles',
            field=models.ManyToManyField(db_constraint=False, related_name='canUseMenus', to='system.role'),
        ),
    ]