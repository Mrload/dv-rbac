# cli/app.py
import typer
app = typer.Typer(help="管理员相关命令")

@app.command("init-super-user")
def init_super_user():
    """
    初始化数据库, 包括超级角色和超级用户
    """
    from .init_super_user import init_super_user_sync
    init_super_user_sync()


@app.command("sync-api-permissions")
def sync_api_permissions():
    """
    同步API权限到数据库
    """
    from .collect_api_permissions import sync_api_permissions
    sync_api_permissions()
