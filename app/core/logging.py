from logging import config as logging_config

from app.core.logging_config import LOGGING_CONFIG


def setup_logging():
    """
    配置日志
    在windows环境下+多Worker模式下日志轮转大概率会报错
    可以尝试使用concurrent-log-handler库来解决这个问题
    """

    logging_config.dictConfig(LOGGING_CONFIG)


# 如果需要自定义access日志，可以如下操作
# import logging
# import time
# from fastapi import Request
# async def access_log_middleware(request: Request, call_next):
#     """
#     访问日志中间件,如果需要自定义access 日志
#     """
#     logger = logging.getLogger("access")
#     start_time = time.time()
#
#     response = await call_next(request)
#
#     cost_ms = int((time.time() - start_time) * 1000)
#
#     logger.info("%s %s %s %s %sms", request.client.host if request.client else "未知IP", request.method, request.url.path, response.status_code, cost_ms)
#
# return response
