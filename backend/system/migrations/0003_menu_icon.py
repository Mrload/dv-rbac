# Generated by Django 4.2 on 2024-03-05 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_alter_role_router_permission_alter_role_user_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='icon',
            field=models.CharField(db_comment='图标', max_length=255, null=True),
        ),
    ]