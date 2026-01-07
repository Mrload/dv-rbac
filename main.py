# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logging import getLogger

from app import model_loader  #  加载所有模型,不能删掉
from app.config import settings
from app.core.database import engine
from app.core.exception_handler import  general_exception_handler
from app.core.apis import router as api_router
from app.core.logging import setup_logging



# 配置日志记录
setup_logging()

logger = getLogger(__name__)

# 定义应用的生命周期管理函数
# 用于在应用关闭时关闭数据库引擎
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 👉 启动逻辑
    logger.info("应用启动...")
    yield
    # 👉 关闭逻辑
    logger.info("关闭数据库引擎...")
    await engine.dispose()
    logger.info("应用关闭完成")

# 创建 FastAPI 应用实例
app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# 注册全局异常处理函数, 处理所有未捕获的异常
app.add_exception_handler(Exception, general_exception_handler)

# 注册 API 路由
app.include_router(api_router)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)