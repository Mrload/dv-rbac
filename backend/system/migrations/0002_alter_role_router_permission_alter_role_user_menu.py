# Generated by Django 4.2 on 2024-03-05 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='router_permission',
            field=models.ManyToManyField(db_constraint=False, db_table='DTP_role_router_permission', related_name='related_roles', to='system.routerpermission'),
        ),
        migrations.AlterField(
            model_name='role',
            name='user',
            field=models.ManyToManyField(db_constraint=False, db_table='DTP_user_role', related_name='roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_comment='路由名称', max_length=255, unique=True)),
                ('alias', models.CharField(db_comment='路由别称', max_length=255)),
                ('url', models.CharField(db_comment='路由地址', max_length=255, unique=True)),
                ('is_catalog', models.BooleanField(db_comment='是否目录', default=False)),
                ('parent', models.ForeignKey(db_column='parent', db_comment='父类ID', db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='system.menu')),
            ],
            options={
                'db_table': 'DTP_menu',
                'db_table_comment': 'Menu表',
            },
        ),
    ]
