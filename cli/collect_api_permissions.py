import asyncio
from fastapi.routing import APIRoute
from sqlalchemy import select
from app.rbac_core.permission.models import Permission
from app.core.database import AsyncSessionLocal

import typer
from main import app
import logging

# main 函数中已经配置了日志, 这里需要重复配置,避免SQL日志干扰
logging.basicConfig(level=logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)



def collect_api_permissions() -> list[dict]:
    permissions = []

    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        if not hasattr(route, "name"):
            typer.echo(f"跳过没有名称的路由：{route.path}")
            continue

        description = route.description if hasattr(route, "description") else None
        summary = route.summary if hasattr(route, "summary") else None

        for method in route.methods:
            if method in {"HEAD", "OPTIONS"}:
                continue

            permissions.append({"name": route.name, "api_path": route.path, "api_method": method, "description": description or summary})

    return permissions


def sync_api_permissions():
    """
    同步API权限到数据库
    """
    permissions = collect_api_permissions()

    async def run():
        async with AsyncSessionLocal() as db:
            for perm in permissions:
                name_existing = await db.execute(select(Permission).where(Permission.name == perm["name"]))
                path_method_existing = await db.execute(select(Permission).where(Permission.api_path == perm["api_path"], Permission.api_method == perm["api_method"]))

                if name_existing.scalar_one_or_none():
                    typer.echo(f"权限已存在-名称重复：{perm['name']}")
                elif path_method_existing.scalar_one_or_none():
                    typer.echo(f"权限已存在-路径方法重复：{perm['api_path']} {perm['api_method']}")
                else:
                    db.add(Permission(**perm))
                    typer.echo(f"添加权限：{perm['name']}")
            await db.commit()

    asyncio.run(run())
