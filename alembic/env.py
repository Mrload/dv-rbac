import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context

from app.config import settings
# 导入你的 ORM Base
# 如果有多个 app，可以导入多个 Base
from app.core.database import Base

# 导入所有模型，确保Alembic能检测到所有表
from app import model_loader 

# 目标元数据，可以是单个或者列表
target_metadata = [Base.metadata]

# Alembic 配置对象
config = context.config
fileConfig(config.config_file_name)

# 数据库 URL 配置
# 可以在 alembic.ini 中配置 sqlalchemy.url
# sqlalchemy.url = sqlite+aiosqlite:///./test.db
# 或 postgresql+asyncpg://user:pass@host/db
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)



def run_migrations_offline():
    """运行离线迁移（生成 SQL 脚本，不连接数据库）"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection):
    """运行迁移的核心函数"""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # 自动检测字段类型变化
        compare_server_default=True,  # 检测默认值变化
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """在线迁移（异步执行）"""
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool
    )

    async with connectable.begin() as conn:
        # 使用 run_sync 包装同步 context 操作
        await conn.run_sync(do_run_migrations)

    await connectable.dispose()

# 根据模式调用
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())