# 异常处理函数
# 将各种异常转换为 HTTP 响应
from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = getLogger("error")


class AppException(Exception):
    """应用程序异常基类"""

    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST, detail: str = "An error occurred"):
        self.detail = detail
        self.status_code = status_code
        super().__init__(self.detail)


async def general_exception_handler(request: Request, exc: Exception):
    """处理通用异常"""
    # 业务逻辑中主动抛出的 AppException 异常，返回其状态码和详情
    if isinstance(exc, AppException):
        logger.error(f"自定义异常: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    # 其他未处理的异常，返回 500 错误
    logger.error(f"未处理异常: {exc}")
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "服务器错误"})
