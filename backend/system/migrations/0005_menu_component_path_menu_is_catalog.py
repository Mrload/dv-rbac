# Generated by Django 4.2 on 2024-03-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_remove_menu_is_catalog'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='component_path',
            field=models.CharField(db_comment='组件地址', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='is_catalog',
            field=models.BooleanField(db_comment='是否目录', default=False),
        ),
    ]
