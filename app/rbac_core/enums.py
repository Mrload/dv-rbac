import enum


class PermissionType(enum.StrEnum):
    menu = "menu"
    action = "action"
    api = "api"


class MenuType(enum.StrEnum):
    DIRECTORY = "directory"   # 目录
    ITEM = "item"             # 可点击菜单