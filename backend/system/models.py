from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# 角色表
class Role(models.Model):
    name = models.CharField(max_length=255,db_comment="角色名",unique=True)
    description = models.TextField(null=True, db_comment='描述信息')
    user = models.ManyToManyField(to=User,related_name="roles",db_table="DTP_user_role",db_constraint=False)
    router_permission = models.ManyToManyField(to="RouterPermission",related_name="related_role",db_table="DTP_role_router_permission",db_constraint=False)
    class Meta:
        db_table = "DTP_role"
        db_table_comment = "角色表"

# api路由表
class Router(models.Model):
    name = models.CharField(max_length=255,db_comment="路由名称",unique=True)
    url = models.CharField(max_length=255,db_comment="路由地址",unique=True)

    class Meta:
        db_table = "DTP_router"
        db_table_comment = "路由表"


# api路由权限表
class RouterPermission(models.Model):

    name = models.CharField(max_length=255,db_comment="权限名称",unique=True)
    router = models.ForeignKey(to="Router",db_constraint=False,on_delete=models.DO_NOTHING,db_comment="关联路由")
    method = models.CharField(max_length=255,db_comment="请求方式")
    
    class Meta:
        db_table = "DTP_router_permission"
        db_table_comment = "路由权限表"

# 前端Menu路由表
class Menu(models.Model):
    name = models.CharField(max_length=255,db_comment="路由名称",unique=True)
    alias = models.CharField(max_length=255,db_comment="路由别称")
    url = models.CharField(max_length=255,db_comment="路由地址",unique=True)
    icon = models.CharField(max_length=255,db_comment="图标",null=True)
    # 这个字段，暂时没用
    parent = models.ForeignKey(null=True,to="self",on_delete=models.DO_NOTHING,db_constraint=False,db_comment="父类ID",db_column="parent")
    # 这个字段，暂时没用
    is_catalog = models.BooleanField(default=False,db_comment="是否目录")
    component_path = models.CharField(max_length=255,db_comment="组件地址",null=True)
    roles = models.ManyToManyField(to=Role, related_name="canUseMenus",db_constraint=False,db_table="DTP_role_menu_permission")  #
    class Meta:
        db_table = "DTP_menu"
        db_table_comment = "Menu表"


# 各类模型表
class Model(models.Model):
    name = models.CharField(max_length=255,db_comment="模型名称",unique=True)
    alias = models.CharField(max_length=255,db_comment="模型别称")
    kind = models.CharField(max_length=255,db_comment="模型类别")
    description = models.TextField(null=True, db_comment='描述信息')

    init_params = models.JSONField(null=True,db_comment="初始参数")

    call_url = models.CharField(max_length=255,db_comment="调用地址")
    call_params = models.JSONField(null=True,db_comment="调用参数")
    
    roles = models.ManyToManyField(to=Role,related_name="models", db_constraint=False,db_table="DTP_role_model_permission")

    class Meta:
        db_table = "DTP_model"
        db_table_comment = "模型表"


