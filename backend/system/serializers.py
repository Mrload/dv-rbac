from rest_framework import serializers

from django.contrib.auth.models import User
from .models import *

# 用户查询序列化
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]

# 用户创建序列化器
class UserCreateSerializer(serializers.ModelSerializer):

    def create(self,validated_data):
        obj = User.objects.create_user(**validated_data)
        return obj

    class Meta:
        model = User
        fields = '__all__'

# 角色序列化器
class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

# api路由序列化器
class RouterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Router
        fields = '__all__'

# api路由权限表
class RouterPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouterPermission
        fields = '__all__'

# 前端Menu序列化器
class MenuSerializer(serializers.ModelSerializer):
    childrens = serializers.SerializerMethodField()
    def get_childrens(self,obj):
        if obj.menu_set.all():
            return MenuSerializer(obj.menu_set.all(),many=True).data

    class Meta:
        model = Menu
        fields = "__all__"
        
